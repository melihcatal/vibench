import os
from google.cloud import storage

client = storage.Client()
bucket_name = os.getenv('GCP_BUCKET_NAME')
bucket = client.get_bucket(bucket_name)

def upload_blob(source_file_name, destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)