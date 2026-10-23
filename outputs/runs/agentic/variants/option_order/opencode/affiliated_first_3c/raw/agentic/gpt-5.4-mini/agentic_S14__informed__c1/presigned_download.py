from typing import Optional

from storage_client import get_bucket_name, get_s3_client, make_object_key


def presigned_download_url(bucket: Optional[str], object_key: str, expires_in: int = 3600) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket or get_bucket_name(), 'Key': make_object_key(object_key)},
        ExpiresIn=expires_in,
    )
