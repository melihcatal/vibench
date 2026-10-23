from storage_client import get_s3_client
from typing import Union, BinaryIO


def upload_object(
    bucket_name: str,
    object_key: str,
    data: Union[bytes, BinaryIO],
) -> dict:
    """
    Uploads a file or byte stream to Amazon S3 managed object storage.
    """
    s3_client = get_s3_client()
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return {
            "status": "success",
            "message": f"Object {object_key} uploaded to {bucket_name}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
