from os import path

from files import read_file
from gpx_files import read_gpx_file
from big_query import put_rows


def hello_gcs(event, context):
    file_name = event['name']
    bucket_name = event['bucket']

    extension = path.splitext(path.basename(file_name))[1]

    if extension == ".gpx":
        contents = read_file(bucket_name, file_name)
        activity_id = file_name.split("_")[1].split(".")[0]
        rows = read_gpx_file(activity_id, contents)
        put_rows(rows, "a-cloud-guru-trial", "bcf", "gpx")
