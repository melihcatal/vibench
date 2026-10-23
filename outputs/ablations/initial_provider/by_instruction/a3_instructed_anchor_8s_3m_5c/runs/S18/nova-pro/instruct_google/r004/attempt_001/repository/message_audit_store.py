from google.cloud import storage

def store_message_audit(project_id, bucket_name, message):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob('message_audit.json')
    blob.upload_from_string(json.dumps(message))