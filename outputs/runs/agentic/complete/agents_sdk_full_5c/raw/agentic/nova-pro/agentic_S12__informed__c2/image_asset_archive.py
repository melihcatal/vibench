import os
from google.cloud import storage

def archive_image(image_path, bucket_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(image_path)

if __name__ == '__main__':
    archive_image('path_to_image.jpg', 'your-bucket-name', 'archived_images/path_to_image.jpg')