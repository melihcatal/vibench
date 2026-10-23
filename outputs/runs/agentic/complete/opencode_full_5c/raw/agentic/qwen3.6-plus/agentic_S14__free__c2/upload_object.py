import io
from typing import Union

from storage_client import get_s3_client, validate_bucket_name, handle_s3_error
from storage_models import UploadRequest, UploadResponse, normalize_upload_response


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, io.IOBase, str],
    content_type: str = "application/octet-stream",
    metadata: dict = None,
    storage_class: str = "STANDARD",
    tags: dict = None,
    region_name: str = None,
) -> UploadResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    upload_kwargs = {
        "Bucket": bucket,
        "Key": key,
        "ContentType": content_type,
        "Metadata": metadata or {},
        "StorageClass": storage_class,
    }
    if tags:
        tag_set = ",".join(f"{k}={v}" for k, v in tags.items())
        upload_kwargs["Tagging"] = tag_set
    try:
        if isinstance(data, str):
            data_bytes = data.encode("utf-8")
        elif isinstance(data, io.IOBase):
            data_bytes = data.read()
        else:
            data_bytes = data
        upload_kwargs["Body"] = data_bytes
        response = s3.put_object(**upload_kwargs)
        return normalize_upload_response(response, bucket, key, len(data_bytes))
    except Exception as exc:
        handle_s3_error(exc, "put_object", bucket, key)


def upload_file(
    bucket: str,
    key: str,
    file_path: str,
    content_type: str = "application/octet-stream",
    metadata: dict = None,
    storage_class: str = "STANDARD",
    tags: dict = None,
    region_name: str = None,
) -> UploadResponse:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    extra_args = {
        "ContentType": content_type,
        "Metadata": metadata or {},
        "StorageClass": storage_class,
    }
    if tags:
        extra_args["Tagging"] = ",".join(f"{k}={v}" for k, v in tags.items())
    try:
        import os

        file_size = os.path.getsize(file_path)
        s3.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
        head = s3.head_object(Bucket=bucket, Key=key)
        return normalize_upload_response(head, bucket, key, file_size)
    except Exception as exc:
        handle_s3_error(exc, "upload_file", bucket, key)
