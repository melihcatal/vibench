import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    """Create a time-limited signed download URL for a stored object in AWS S3."""
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for GET operation
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket, "Key": request.object_key},
            ExpiresIn=request.expiration_seconds or 3600,  # Default 1 hour
        )

        return PresignedUrlResponse(
            success=True,
            presigned_url=presigned_url,
            bucket=request.bucket,
            object_key=request.object_key,
            expiration_seconds=request.expiration_seconds or 3600,
            message="Presigned URL generated successfully",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False, error_message=f"AWS S3 error: {str(e)}"
        )
    except Exception as e:
        return PresignedUrlResponse(
            success=False, error_message=f"Failed to generate presigned URL: {str(e)}"
        )
