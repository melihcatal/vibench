import os
from google.cloud import storage

client = storage.Client(os.getenv('GOOGLE_CLOUD_API_KEY'))
bucket = client.get_bucket('my-export-bucket')

def export_record(record_id, record_data):
    blob = bucket.blob(record_id)
    blob.upload_from_string(record_data)