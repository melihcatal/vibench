from google.cloud import storage
import json

def archive_asset(bucket_name, destination_blob_name, data_to_archive):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert data to JSON string for archiving
    if isinstance(data_to_archive, dict):
        content = json.dumps(data_to_archive, indent=2)
        blob.upload_from_string(content, content_type='application/json')
    else:
        # Assume it's a string if not a dict, or handle other types as needed
        blob.upload_from_string(str(data_to_archive), content_type='text/plain')

    return f"gs://{bucket_name}/{destination_blob_name}"
