from storage_models import PresignedUrlRequest
from storage_client import (
    get_storage_client,
    get_bucket,
    create_blob,
    generate_signed_url,
)


def create_presigned_download_url(bucket_name, object_name, expiration_minutes=60):
    request = PresignedUrlRequest(
        bucket=bucket_name,
        object_name=object_name,
        expiration_minutes=expiration_minutes,
    )
    client = get_storage_client()
    bucket = get_bucket(client, request.bucket)
    blob = create_blob(bucket, request.object_name)
    signed_url = generate_signed_url(
        blob, expiration_minutes=request.expiration_minutes
    )
    return {
        "url": signed_url,
        "bucket": request.bucket,
        "object_name": request.object_name,
        "expiration_minutes": request.expiration_minutes,
    }
