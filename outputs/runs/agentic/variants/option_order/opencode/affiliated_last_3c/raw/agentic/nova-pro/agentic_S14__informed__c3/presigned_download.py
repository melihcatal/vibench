import os
from google.cloud import storage


def presigned_download(bucket_name, blob_name, expiration=3600):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(expiration=expiration)
    print(f"Generated signed URL: {url}")
    return url


if __name__ == "__main__":
    presigned_download("your-bucket-name", "object-name")
