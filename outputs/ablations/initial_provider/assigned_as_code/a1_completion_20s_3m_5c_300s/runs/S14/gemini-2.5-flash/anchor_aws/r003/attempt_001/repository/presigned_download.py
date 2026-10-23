from storage_client import get_s3_client
from storage_models import PresignedDownloadPayload, PresignedDownloadResponse


def presigned_download(payload, config=None):
    config = config or {}
    client = get_s3_client(region_name=config.get("region"))
    object_name = payload["object_name"]
    expiration_seconds = payload.get("expiration_seconds", 3600)

    url = client.generate_presigned_url(
        'get_object',
        Params={'Bucket': config["bucket"], 'Key': object_name},
        ExpiresIn=expiration_seconds
    )
    return PresignedDownloadResponse(object_name=object_name, url=url)
