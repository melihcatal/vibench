from google.cloud import storage
import os

def record_export_archive(payload, config=None):
    config = config or {}
    storage_client = storage.Client()
    
    bucket_name = config["bucket_name"]
    destination_blob_name = payload["archive_path"]
    data_to_archive = payload["document_content"]

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data_to_archive)
    
    return {"archive_path": f"gs://{bucket_name}/{destination_blob_name}", "status": "success"}
