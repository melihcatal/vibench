from google.cloud import storage

def archive_image(image_path, bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(image_path.split('/')[-1])
    blob.upload_from_filename(image_path)
    print('Image archived in', bucket_name)