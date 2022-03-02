resource "google_bigquery_dataset" "dataset" {
  dataset_id    = "bcf"
  location      = "EUROPE-WEST2"

  access {
    role          = "OWNER"
    user_by_email = "death.tumble@gmail.com"
  }
  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }
  access {
    role          = "READER"
    special_group = "projectReaders"
  }
  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }

  timeouts {}

}


resource "google_bigquery_table" "gpx" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "gpx"

  labels = {
  }

  schema = <<-SCHEMA
    [
        {
            "mode":"NULLABLE",
            "name":"effort",
            "type":"INTEGER"
        },
        {
            "mode":"NULLABLE",
            "name":"time",
            "type":"TIMESTAMP"
        },
        {
            "mode":"NULLABLE",
            "name":"cad",
            "type":"INTEGER"
        },
        {
            "mode":"NULLABLE",
            "name":"hr",
            "type":"INTEGER"
        },
        {
            "mode":"NULLABLE",
            "name":"ele",
            "type":"INTEGER"
        },
        {
            "mode":"NULLABLE",
            "name":"lat",
            "type":"FLOAT"
        },
        {
            "mode":"NULLABLE",
            "name":"long",
            "type":"FLOAT"
        }
    ]  
SCHEMA
}
