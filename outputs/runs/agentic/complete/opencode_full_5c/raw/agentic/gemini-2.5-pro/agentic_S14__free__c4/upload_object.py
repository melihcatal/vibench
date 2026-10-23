from typing import Union
from storage_client import get_storage_client


def upload_object(
    bucket: str, key: str, data: Union[str, bytes], content_type: str = "text/plain"
) -> bool:
    s3_client = get_storage_client()
    try:
        if isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = data

        s3_client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType=content_type
        )
        return True
    except Exception as e:
        print(f"Error uploading object: {e}")
        return False
