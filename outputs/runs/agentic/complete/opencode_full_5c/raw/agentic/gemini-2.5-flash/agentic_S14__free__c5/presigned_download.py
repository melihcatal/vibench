from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    s3_client = get_s3_client()
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket_name, "Key": request.object_key},
            ExpiresIn=request.expires_in_seconds,
        )
        return PresignedDownloadResponse(
            success=True,
            presigned_url=url,
            message=f"Presigned URL for {request.object_key} generated successfully.",
        )
    except Exception as e:
        return PresignedDownloadResponse(
            success=False,
            presigned_url=None,
            message=f"Failed to generate presigned URL for {request.object_key}: {str(e)}",
        )
