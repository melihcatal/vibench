import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    """
    Creates a time-limited signed download URL for a stored object in AWS S3.
    """
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for S3 object
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket, "Key": request.object_key},
            ExpiresIn=request.expiration_seconds or 3600,  # Default 1 hour
        )

        return PresignedUrlResponse(
            success=True,
            presigned_url=presigned_url,
            object_key=request.object_key,
            bucket=request.bucket,
            expiration_seconds=request.expiration_seconds or 3600,
            message=f"Generated presigned URL for s3://{request.bucket}/{request.object_key}",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to generate presigned URL from AWS S3: {e}",
        )
