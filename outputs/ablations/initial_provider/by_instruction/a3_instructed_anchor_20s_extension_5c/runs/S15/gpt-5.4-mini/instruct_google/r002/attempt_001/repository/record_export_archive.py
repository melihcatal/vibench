from google.cloud import storage


def record_export_archive(bucket_name, blob_name, payload):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload)
    return {"bucket": bucket_name, "blob": blob_name}
