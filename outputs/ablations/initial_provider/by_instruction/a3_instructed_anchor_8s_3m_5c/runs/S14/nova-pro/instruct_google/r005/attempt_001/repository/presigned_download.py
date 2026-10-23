from google.cloud import storage

def presigned_download(bucket_name, blob_name, expiration):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(expiration=expiration)
    print(f"Generated signed URL: {url}")
    return url
