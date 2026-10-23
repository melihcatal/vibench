from google.cloud import storage

def archive_image_asset(payload, config=None):
    config = config or {}
    client = storage.Client()
    
    bucket_name = payload["bucket_name"]
    destination_blob_name = payload["destination_blob_name"]
    image_bytes = payload["image_bytes"]
    metadata = payload.get("metadata", {})

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(image_bytes, content_type="image/jpeg")
    blob.metadata = metadata
    blob.patch()

    return {"gcs_uri": f"gs://{bucket_name}/{destination_blob_name}"}
