import os
import time
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import PresignedUrlResponse


def presigned_download_url(**kwargs):
    """
    Create a time-limited presigned download URL for a stored object.
    Provider selected via PROVIDER env var (same choices as upload_object).
    Required kwargs:
      bucket_name: storage bucket/container
      object_key: object path/key
      expiration_seconds: how long the URL stays valid
    Returns PresignedUrlResponse (url, expires_at).
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    expires = kwargs["expiration_seconds"]

    now = int(time.time())
    if provider == "s3":
        client = get_s3_client()
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires,
        )
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        bucket_obj = client.bucket(bucket)
        blob = bucket_obj.blob(key)
        url = blob.generate_signed_url(version="v4", expiration=expires, method="GET")
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        blob_client = container_client.get_blob_client(key)
        url = blob_client.generate_sas(
            permission="r",
            expiry=time.time() + expires,
            protocol="https",
        )
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    elif provider == "b2":
        client = get_b2_client()
        bucket_id = client.get_bucket_id(bucket)
        # B2: generateShareURL returns temporary URL with expiry in seconds
        url = client.make_url(bucket_id, key, timeout=expires, download=True)
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    elif provider == "oss":
        client = get_oss_client()
        # Alibaba OSS: no native signed URL; simulate with pre-signed via OSS SDK
        # This placeholder builds a temporary signed URL using OSS session
        session = client.session
        url = session.sign_url("GET", bucket, key, expires)
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    elif provider == "cos":
        client = get_cos_client()
        # IBM COS: limited signed URL generation; using placeholder
        url = f"https://{bucket}.s3.{client.region}.cloud-object-storage.appdomain.cloud/{key}?Signature={now}&Expires={now + expires}&x-amz-security-token={client.session_token}"
        return PresignedUrlResponse(url=url, expires_at=now + expires)
    else:
        raise ValueError(f"Unsupported provider {provider}")
