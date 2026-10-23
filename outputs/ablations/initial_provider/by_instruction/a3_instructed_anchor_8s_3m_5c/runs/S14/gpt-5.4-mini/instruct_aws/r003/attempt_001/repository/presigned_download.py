from typing import Optional

from storage_client import get_s3_client


def presigned_download(bucket: str, key: str, expires_in: int = 3600, region: Optional[str] = None) -> str:
    s3 = get_s3_client(region)
    return s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in)
