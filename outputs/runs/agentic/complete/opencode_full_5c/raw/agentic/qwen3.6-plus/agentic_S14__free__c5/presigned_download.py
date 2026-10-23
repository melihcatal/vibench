from datetime import datetime, timedelta, timezone
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, handle_aws_error
from storage_models import StorageConfig, PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    http_method: str = "GET",
    config: Optional[StorageConfig] = None,
) -> PresignedUrlResponse:
    s3_client = get_s3_client(config)

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket,
                "Key": key,
            },
            ExpiresIn=expires_in,
            HttpMethod=http_method,
        )

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        return PresignedUrlResponse(
            success=True,
            url=url,
            expires_at=expires_at,
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False,
            error=handle_aws_error(e, "presigned_download_url"),
        )
    except Exception as e:
        return PresignedUrlResponse(
            success=False,
            error=f"presigned_download_url error: {str(e)}",
        )


def create_presigned_download_from_request(
    request: PresignedUrlRequest,
    config: Optional[StorageConfig] = None,
) -> PresignedUrlResponse:
    return create_presigned_download_url(
        bucket=request.bucket,
        key=request.key,
        expires_in=request.expires_in,
        http_method=request.http_method,
        config=config,
    )
