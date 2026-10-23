from storage_client import default_expires_in, get_s3_client
from storage_models import PresignedUrlResponse, StorageObjectRef


def presigned_download(ref: StorageObjectRef, expires_in: int | None = None) -> PresignedUrlResponse:
    client = get_s3_client()
    ttl = default_expires_in() if expires_in is None else expires_in
    url = client.generate_presigned_url("get_object", Params={"Bucket": ref.bucket, "Key": ref.key}, ExpiresIn=ttl)
    return PresignedUrlResponse(bucket=ref.bucket, key=ref.key, url=url, expires_in=ttl)
