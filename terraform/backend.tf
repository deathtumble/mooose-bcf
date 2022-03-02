terraform {
  backend "gcs" {
    bucket  = "moose_bcf_terraform_state"
    prefix  = "terraform/bcf"
  }
}