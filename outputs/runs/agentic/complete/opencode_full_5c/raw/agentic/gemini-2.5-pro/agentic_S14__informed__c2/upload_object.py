import os
from storage_client import get_storage_client


def upload_file_to_s3(bucket_name: str, object_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} was not found.")

    s3_client = get_storage_client()
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return {"status": "success", "bucket": bucket_name, "object_name": object_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def upload_bytes_to_s3(bucket_name: str, object_name: str, data: bytes):
    """
    Uploads a byte stream to an S3 bucket.
    """
    s3_client = get_storage_client()
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)
        return {"status": "success", "bucket": bucket_name, "object_name": object_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
