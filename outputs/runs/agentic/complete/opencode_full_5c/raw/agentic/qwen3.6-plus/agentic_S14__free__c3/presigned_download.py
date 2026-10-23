from datetime import datetime, timedelta

from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_name, PRESIGNED_URL_EXPIRY
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(request: PresignedUrlRequest) -> PresignedUrlResponse:
    s3_client = get_s3_client()
    validate_bucket_name(request.bucket)

    expiry = (
        request.expiry_seconds if request.expiry_seconds > 0 else PRESIGNED_URL_EXPIRY
    )

    params = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if request.response_content_disposition:
        params["ResponseContentDisposition"] = request.response_content_disposition

    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=expiry,
            HttpMethod=request.http_method,
        )

        expires_at = datetime.utcnow() + timedelta(seconds=expiry)

        return PresignedUrlResponse(
            success=True,
            url=url,
            expires_at=expires_at,
        )
    except ClientError as e:
        return PresignedUrlResponse(
            success=False,
            error=f"AWS S3 presigned URL generation failed: {e.response['Error']['Code']} - {e.response['Error']['Message']}",
        )
    except Exception as e:
        return PresignedUrlResponse(
            success=False,
            error=str(e),
        )
