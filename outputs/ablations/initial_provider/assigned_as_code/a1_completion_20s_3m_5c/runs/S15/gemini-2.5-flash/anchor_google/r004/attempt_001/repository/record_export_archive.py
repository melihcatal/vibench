from google.cloud import storage

def record_export_archive(bucket_name, destination_blob_name, data, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {"bucket": bucket_name, "blob": destination_blob_name, "status": "uploaded"}
