import os
from google.cloud import storage

client = storage.Client()

def export_metrics(bucket_name, source_blob_name, destination_blob_name):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.copy_to(destination_blob_name)