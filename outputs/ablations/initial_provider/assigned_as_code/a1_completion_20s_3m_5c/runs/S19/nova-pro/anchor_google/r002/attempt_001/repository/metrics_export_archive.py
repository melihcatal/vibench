from google.cloud import storage

def metrics_export_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.get_bucket(config['bucket_name'])
    blob = bucket.blob(payload['file_name'])
    blob.upload_from_string(payload['content'])
    return {"file_name": payload['file_name']}