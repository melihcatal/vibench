from storage_client import create_s3_client, resolve_bucket
from storage_models import PresignedDownloadRequest


def presigned_download(bucket: str, key: str, expires_in: int = 900):
    request = PresignedDownloadRequest(
        bucket=bucket, key=key, expires_in=expires_in
    ).normalize()
    s3 = create_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": resolve_bucket(request.bucket), "Key": request.key},
        ExpiresIn=request.expires_in,
    )
