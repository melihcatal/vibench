from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from botocore.exceptions import ClientError


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    s3_client = StorageClient().get_s3_client()
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket_name, "Key": request.object_key},
            ExpiresIn=request.expiration,
        )
        return PresignedDownloadResponse(
            success=True, url=url, message="Presigned URL generated successfully."
        )
    except ClientError as e:
        return PresignedDownloadResponse(
            success=False, url=None, message=f"Error generating presigned URL: {e}"
        )
