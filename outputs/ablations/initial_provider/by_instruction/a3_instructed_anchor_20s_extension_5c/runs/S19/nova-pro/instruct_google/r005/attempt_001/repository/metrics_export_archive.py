from google.cloud import storage

def export_metrics_to_storage(bucket_name, file_name, content):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content)
