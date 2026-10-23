from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket_name, "Key": request.key},
            ExpiresIn=request.expiration_seconds,
        )
        return PresignedDownloadResponse(presigned_url=response)
    except Exception as e:
        raise RuntimeError(
            f"Failed to generate presigned URL for {request.key} in {request.bucket_name}: {e}"
        )
