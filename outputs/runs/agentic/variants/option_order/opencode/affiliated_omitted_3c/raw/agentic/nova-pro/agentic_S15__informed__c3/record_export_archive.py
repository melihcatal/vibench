import os
from google.cloud import storage


def export_archive(data, filename):
    client = storage.Client()
    bucket = client.bucket(os.getenv("GOOGLE_CLOUD_BUCKET"))
    blob = bucket.blob(filename)
    blob.upload_from_string(data)
