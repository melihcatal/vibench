import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    """
    Creates a time-limited signed download URL for an object stored in AWS S3.
    """
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for S3 object
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket, "Key": request.key},
            ExpiresIn=request.expiration_seconds,
        )

        return PresignedUrlResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            presigned_url=url,
            expiration_seconds=request.expiration_seconds,
            message=f"Presigned URL generated for s3://{request.bucket}/{request.key}",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"S3 presigned URL error: {str(e)}",
        )
    except Exception as e:
        return PresignedUrlResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Presigned URL error: {str(e)}",
        )
