from google.cloud import storage


def read_file(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    return bucket.get_blob(file_name).download_as_string()
