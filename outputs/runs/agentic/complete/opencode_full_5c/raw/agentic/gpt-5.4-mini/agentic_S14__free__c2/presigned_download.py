from storage_client import storage_client
from storage_models import SignedUrlResponse


def presigned_download(
    bucket: str, object_name: str, expires_in: int = 3600
) -> SignedUrlResponse:
    client = storage_client("s3")
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": object_name},
        ExpiresIn=expires_in,
    )
    return SignedUrlResponse(
        bucket=bucket,
        object_name=object_name,
        url=url,
        expires_in=expires_in,
        raw={"url": url},
    )
