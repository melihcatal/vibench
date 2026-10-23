from datetime import datetime, timedelta
from b2sdk.v2 import B2Api
from storage_client import get_b2_client, get_bucket_name
from storage_models import PresignedDownloadResponse


def create_presigned_download_url(object_name: str, expires_in: int = 3600) -> PresignedDownloadResponse:
    b2_api: B2Api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    url = b2_api.get_download_url_for_file_name(
        bucket_name=get_bucket_name(),
        file_name=object_name
    )
    
    # B2 does not natively support presigned URLs, so we use the download URL directly
    # with an expiration timestamp in the response model.
    expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    return PresignedDownloadResponse(
        url=url,
        expires_at=expires_at
    )