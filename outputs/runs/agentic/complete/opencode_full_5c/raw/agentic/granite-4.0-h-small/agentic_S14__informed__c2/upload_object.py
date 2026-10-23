import os
from typing import BinaryIO, Optional


def upload_object(
    provider: str,
    bucket: str,
    key: str,
    data: BinaryIO,
    content_type: Optional[str] = None,
) -> str:
    """
    Upload a file or byte stream to the configured managed object storage.

    Returns the remote object identifier (e.g., file ID or object key) that can be referenced later.
    """
    provider_name = StorageClient.get_provider_name()
    config = StorageClient.PROVIDERS[provider_name]
    sdk = config["sdk"]

    if provider_name == "backblaze_b2":
        import b2sdk.v1 as b2

        app_key_id = os.getenv("B2_APPLICATION_KEY_ID")
        app_key = os.getenv("B2_APPLICATION_KEY")
        b2_api = b2.B2Api()
        b2_api.authorize_account("production", app_key_id, app_key)
        bucket_id = b2_api.get_bucket_id_by_name(bucket)
        b2_api.upload_file(
            file_name=key,
            bucket_id=bucket_id,
            file_data=data,
            content_type=content_type,
        )
        return bucket_id
    elif provider_name == "amazon_s3":
        import boto3
        import botocore

        session = boto3.session.Session()
        s3 = session.client(
            "s3",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        try:
            s3.upload_fileobj(
                Fileobj=data,
                Bucket=bucket,
                Key=key,
                ExtraArgs={"ContentType": content_type},
            )
        except botocore.exceptions.ClientError:
            raise
        return bucket + "/" + key
    else:
        raise NotImplementedError(
            f"Upload not implemented for provider {provider_name}"
        )
