import os
from google.cloud import storage


def list_prefix(bucket_name, prefix=""):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    for blob in blobs:
        print(blob.name)


if __name__ == "__main__":
    list_prefix("your-bucket-name", "prefix/")
