from storage_client import get_s3_client
from storage_models import PresignedUrlResult


def create_presigned_download_url(bucket_name: str, object_name: str, expiration: int = 3600, config: dict = None) -> PresignedUrlResult:
    config = config or {}
    s3_client = get_s3_client(region_name=config.get("region"))
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration
    )
    return PresignedUrlResult(url=url)
