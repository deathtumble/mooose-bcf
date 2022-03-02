resource "google_storage_bucket" "bucket" {
  name     = "moose_bcf_builds"
  location = "EUROPE-WEST2"
  labels = {}
}

data "google_storage_bucket_object" "archive" {
  bucket = google_storage_bucket.bucket.name
  name = "builds/function/refs/heads/feature/gpx-file/function.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "gpx_to_bigquery"
  runtime     = "python38"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = data.google_storage_bucket_object.archive.name
  entry_point           = "hello_gcs"
  
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource = "bcf"
    failure_policy {
      retry = false
    }
  }

  labels = {
    "deployment-tool" = "cli-gcloud"
  }

  lifecycle {
      ignore_changes = [
        labels.deployment-tool,
        event_trigger[0].resource
      ]
  }
}
