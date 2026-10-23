import os
from typing import Optional


def presigned_download_url(
    provider: str, bucket: str, key: str, expires_seconds: int = 3600
) -> str:
    """
    Create a time-limited signed URL for downloading a stored object.

    Returns the presigned URL as a string.
    """
    provider_name = StorageClient.get_provider_name()
    config = StorageClient.PROVIDERS[provider_name]
    sdk = config["sdk"]

    if provider_name == "backblaze_b2":
        from b2sdk.v1 import B2Api, DownloadFileByUrl

        app_key_id = os.getenv("B2_APPLICATION_KEY_ID")
        app_key = os.getenv("B2_APPLICATION_KEY")
        b2_api = B2Api()
        b2_api.authorize_account("production", app_key_id, app_key)
        url = b2_api.make_presigned_download_url(
            bucket, key, expiration=expires_seconds
        )
        return url
    elif provider_name == "amazon_s3":
        import boto3
        import botocore

        session = boto3.session.Session()
        s3_client = session.client(
            "s3",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_seconds,
        )
        return url
    else:
        raise NotImplementedError(
            f"Presigned download not implemented for provider {provider_name}"
        )
