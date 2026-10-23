from storage_client import get_s3_client, raise_storage_error
from storage_models import PresignedDownloadRequest


def presigned_download(bucket: str, key: str, expires_in: int = 3600) -> str:
    request = PresignedDownloadRequest(bucket=bucket, key=key, expires_in=expires_in)
    try:
        return get_s3_client().generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": request.bucket, "Key": request.key},
            ExpiresIn=request.expires_in,
        )
    except Exception as exc:
        raise raise_storage_error(exc)
