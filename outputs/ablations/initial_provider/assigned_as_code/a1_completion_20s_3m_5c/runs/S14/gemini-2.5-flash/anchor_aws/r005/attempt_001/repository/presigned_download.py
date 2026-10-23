import os
from storage_client import get_s3_client


def create_presigned_download_url(payload, config=None):
    config = config or {}
    bucket_name = config.get("bucket", os.environ.get("AWS_S3_BUCKET_NAME"))
    object_name = payload["object_name"]
    expiration = payload.get("expiration", 3600)  # Default to 1 hour

    s3_client = get_s3_client(config.get("region"))

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return {"presigned_url": response}
    except Exception as e:
        raise RuntimeError(f"Error generating presigned URL: {e}")
