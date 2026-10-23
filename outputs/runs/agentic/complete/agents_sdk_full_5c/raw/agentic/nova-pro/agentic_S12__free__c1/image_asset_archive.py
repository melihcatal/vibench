import os
from google.cloud import storage

def archive_image(image_path, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(os.path.basename(image_path))
    blob.upload_from_filename(image_path)