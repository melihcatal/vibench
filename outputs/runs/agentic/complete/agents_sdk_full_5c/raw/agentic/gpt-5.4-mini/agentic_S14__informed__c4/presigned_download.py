from __future__ import annotations

from storage_client import coerce_bucket, get_s3_client
from storage_models import SignedUrlRequest


def presigned_download(request: SignedUrlRequest) -> str:
    client = get_s3_client()
    bucket = coerce_bucket(request.bucket)
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": request.key},
        ExpiresIn=request.expires_in_seconds,
    )
