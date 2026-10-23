import os
from typing import List


def list_objects_under_prefix(provider: str, bucket: str, prefix: str) -> List[str]:
    """
    List object keys stored under a bucket or container prefix.

    Returns a list of key strings.
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
        files = b2_api.list_file_names(
            bucket_id, start_file_name=prefix, max_file_count=1000
        )
        return [prefix.rstrip("/") + "/" + name for name in files]
    elif provider_name == "amazon_s3":
        import boto3
        import botocore

        session = boto3.session.Session()
        s3 = session.client(
            "s3",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        keys = []
        for page in pages:
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])
        return keys
    else:
        raise NotImplementedError(
            f"List prefix not implemented for provider {provider_name}"
        )
