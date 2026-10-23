import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import UploadResponse


def upload_object(**kwargs):
    """
    Upload a file or byte stream to managed object storage.
    Choose provider by setting PROVIDER env var:
      "s3", "gcs", "azure", "b2", "oss", "cos"
    Required kwargs:
      provider: one of the above
      bucket_name: destination bucket
      object_key: destination key/path
      file_path: local file to upload (str) OR
      data: bytes/bytearray to upload
    Returns UploadResponse.
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set to select storage service")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    file_path = kwargs.get("file_path")
    data = kwargs.get("data")
    if not file_path and not data:
        raise ValueError("Must provide either file_path or data")

    if provider == "s3":
        client = get_s3_client()
        if file_path:
            client.upload_file(file_path, bucket, key)
        else:
            client.put_object(Bucket=bucket, Key=key, Body=data)
        return UploadResponse(bucket_name=bucket, object_key=key, etag=None)
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        blob = client.bucket(bucket).blob(key)
        if file_path:
            blob.upload_from_filename(file_path)
        else:
            blob.upload_from_string(data)
        return UploadResponse(
            bucket_name=bucket,
            object_key=key,
            etag=client.get_bucket(bucket).get_blob(key).generation,
        )
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        if file_path:
            container_client.upload_blob(key, open(file_path, "rb"))
        else:
            container_client.upload_blob(key, data)
        blob = container_client.get_blob_client(key)
        return UploadResponse(
            bucket_name=bucket, object_key=key, etag=blob.properties.etag
        )
    elif provider == "b2":
        client = get_b2_client()
        bucket_id = client.get_bucket_id(bucket)
        if file_path:
            client.upload_file(bucket_id, key, file_path)
        else:
            client.upload_file(bucket_id, key, data)
        # B2 API does not return etag directly; returning placeholder
        return UploadResponse(bucket_name=bucket, object_key=key, etag="placeholder")
    elif provider == "oss":
        client = get_oss_client()
        if file_path:
            client.put_object_from_file(key, file_path)
        else:
            client.put_object(key, data)
        return UploadResponse(bucket_name=bucket, object_key=key, etag="placeholder")
    elif provider == "cos":
        client = get_cos_client()
        if file_path:
            client.upload_file(bucket, key, file_path)
        else:
            client.upload_object(bucket, key, data)
        return UploadResponse(bucket_name=bucket, object_key=key, etag="placeholder")
    else:
        raise ValueError(f"Unknown provider {provider}")
