from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse
from botocore.exceptions import ClientError


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    s3_client = get_s3_client()
    try:
        # The AWS S3 client generates the presigned URL.
        # This URL grants temporary access to the object.
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket_name, "Key": request.object_key},
            ExpiresIn=request.expiration_seconds,
        )
        return PresignedDownloadResponse(
            success=True,
            message="Presigned URL generated successfully",
            presigned_url=presigned_url,
        )
    except ClientError as e:
        return PresignedDownloadResponse(
            success=False, message=f"AWS S3 ClientError: {e}"
        )
    except Exception as e:
        return PresignedDownloadResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
