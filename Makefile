PYTHON_VERSION ?= 3.8.12
PIP ?= pip3
POETRY ?= poetry $(POETRY_OPTS)
ACTIVATE ?= . .venv/bin/activate
BUILD_DIR := build
TERRAFORM_DIR := terraform
BUILD_BUCKET ?= moose_bcf_builds
ARTIFACT_NAME = function

python_objects= $(shell find mooose-bcf/ -type f -name '*.py')

GIT_REF ?= refs/heads/$(shell git rev-parse --abbrev-ref HEAD)
GIT_SHA ?= $(shell git rev-parse HEAD)
SHA1_START := $(shell echo ${GIT_SHA} | cut -c -2)
SHA1_END := $(shell echo ${GIT_SHA} | cut -c 3-)
GIT_DIRTY ?= $(if $(shell git diff --stat),true,false)
GIT_REF_TYPE ?= branch

BUILD_OBJECT_LOCATION = gs://${BUILD_BUCKET}/builds/${ARTIFACT_NAME}/objects/${SHA1_START}/${SHA1_END}
BUILD_REF_LOCATION = gs://${BUILD_BUCKET}/builds/${ARTIFACT_NAME}/${GIT_REF}

RAND = $(shell ${RANDOM})

.PHONY: unittest install-python install-poetry

clean-terraform:
	rm -f terraform/.terraform

clean:
	rm -rf build
	rm -rf .venv

.venv/bin:
	python3 -m venv .venv
	. .venv/bin/activate
	python3 -m pip install poetry
	poetry install
	touch .venv/bin

poetry.lock: pyproject.toml poetry.toml
	. .venv/bin/activate \
	poetry lock
	touch poetry.lock

.venv/lib: poetry.lock pyproject.toml poetry.toml
	poetry install
	touch .venv/lib

.venv: .venv/bin .venv/lib
	touch .venv

install-python: .venv
	
install: install-python

unittest: .venv
	${ACTIVATE} && GIT_REF=${GIT_REF} ${POETRY} run pytest --junitxml=${BUILD_DIR}/test-reports/unittest.xml --html=${BUILD_DIR}/test-reports/html/unittest.html

${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}

${BUILD_DIR}/function: ${python_objects}
	mkdir -p ${BUILD_DIR}/function
	rm -rf ${BUILD_DIR}/function/*
	rsync -a mooose-bcf/* build/function --exclude "*__pycache__*" --exclude "*tests*"

${BUILD_DIR}/function/requirements.txt: poetry.lock pyproject.toml poetry.toml ${BUILD_DIR}/function
	poetry export -o build/function/requirements.txt --without-hashes	

build/function.zip: ${python_objects} ${BUILD_DIR}/function/requirements.txt
	echo ${python_objects}
	rm -f $@
	cd ${BUILD_DIR}/function && zip -ur ../function.zip *

upload-function: ${BUILD_DIR}/function.zip
	@if [ "${GIT_DIRTY}" = "false" ]; then \
		gsutil cp ${BUILD_DIR}/function.zip ${BUILD_OBJECT_LOCATION}/function.zip; \
	fi

	if [ "${GIT_REF_TYPE}" = "branch" ] || [ "${GIT_DIRTY}" = "false" ]; then \
		gsutil cp ${BUILD_DIR}/function.zip ${BUILD_REF_LOCATION}/function.zip; \
	fi

redeploy: upload-builds
	gcloud functions deploy gpx_to_bigquery \
	--entry-point hello_gcs \
	--runtime python38 \
	--project a-cloud-guru-trial \
	--trigger-event google.storage.object.finalize \
	--trigger-resource bcf \
	--source ${BUILD_REF_LOCATION}/function.zip \
	--clear-labels \
	--region europe-west1 


build/sync/out:
	mkdir -p build/sync/out

send-gpx: build/sync/out
	cp data/sample.gpx build/sync/out/activity_$$(date +'%Y%m%d%H%M%S').gpx 
	printf 'Upload finished %s\n' "$$(date --iso=seconds)"

send-fit: build/sync/out
	cp data/sample.fit build/sync/out/$$(date +'%Y-%m-%d-%H-%M-%S').fit
	printf 'Creation finished %s\n' "$$(date --iso=seconds)"

auth:
	gcloud auth application-default login

terraform/.terraform:
	cd ${TERRAFORM_DIR} && terraform init

tf-workspace-%: terraform/.terraform
	cd ${TERRAFORM_DIR} && terraform workspace list && terraform workspace select $*

tf-init: terraform/.terraform
	cd ${TERRAFORM_DIR} && terraform workspace list && terraform init

tf-plan: terraform/.terraform
	cd ${TERRAFORM_DIR} && terraform workspace list && terraform plan

tf-apply: terraform/.terraform
	cd ${TERRAFORM_DIR} && terraform workspace list && terraform apply

tf-apply-refresh: terraform/.terraform
	cd ${TERRAFORM_DIR} && terraform workspace list && terraform apply -refresh-only