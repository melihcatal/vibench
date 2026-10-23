import os
from storage_client import get_s3_client

def upload_object(bucket_name, object_key, file_path=None, data=None):
    """Upload a file or byte stream to Amazon S3.
    """
    s3 = get_s3_client()
    if file_path:
        s3.upload_file(file_path, bucket_name, object_key)
    elif data:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    else:
        raise ValueError('Provide either file_path or data to upload')