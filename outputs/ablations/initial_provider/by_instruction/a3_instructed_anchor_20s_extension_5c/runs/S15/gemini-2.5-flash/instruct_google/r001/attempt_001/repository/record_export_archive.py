from google.cloud import storage

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {"status": "success", "bucket": bucket_name, "blob": destination_blob_name}