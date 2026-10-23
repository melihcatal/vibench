import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    """Create a time-limited signed download URL for an object in AWS S3."""
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for S3 object
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket, "Key": request.object_key},
            ExpiresIn=request.expiration_seconds,
        )

        return PresignedUrlResponse(
            success=True,
            presigned_url=presigned_url,
            object_key=request.object_key,
            bucket=request.bucket,
            expiration_seconds=request.expiration_seconds,
            message=f"Generated AWS S3 presigned URL valid for {request.expiration_seconds} seconds",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to generate AWS S3 presigned URL: {e.response['Error']['Code']}",
        )
    except Exception as e:
        return PresignedUrlResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to generate presigned URL: {str(e)}",
        )
