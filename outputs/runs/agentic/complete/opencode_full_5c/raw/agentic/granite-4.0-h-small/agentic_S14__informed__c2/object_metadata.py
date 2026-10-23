import os
from .storage_models import GenericObjectMetadata
from typing import Optional


def get_object_metadata(provider: str, bucket: str, key: str) -> GenericObjectMetadata:
    """
    Retrieve object metadata (or HEAD information) for a stored object.

    Returns a normalized GenericObjectMetadata instance.
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
        info = b2_api.get_file_info_from_bucket(bucket_id, key)
        return GenericObjectMetadata(
            bucket=bucket,
            key=key,
            size=info.content_length,
            etag=info.file_id,
            last_modified=str(info.upload_timestamp),
            content_type=info.content_type,
        )
    elif provider_name == "amazon_s3":
        import boto3
        import botocore

        session = boto3.session.Session()
        s3 = session.client(
            "s3",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        response = s3.head_object(Bucket=bucket, Key=key)
        return GenericObjectMetadata(
            bucket=bucket,
            key=key,
            size=response["ContentLength"],
            etag=response["ETag"].strip('"'),
            last_modified=response["LastModified"].isoformat(),
            content_type=response.get("ContentType"),
        )
    else:
        raise NotImplementedError(
            f"Metadata retrieval not implemented for provider {provider_name}"
        )
