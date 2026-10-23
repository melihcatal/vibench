from google.cloud import storage

def create_presigned_url(bucket_name, object_name, expiration=3600):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    url = blob.generate_signed_url(expiration=expiration, method='GET')
    return url