import os
import io
from typing import Optional, Union

from botocore.exceptions import ClientError

from storage_client import get_s3_client, handle_aws_error
from storage_models import StorageConfig, UploadRequest, UploadResponse


def upload_object(
    source: Union[str, bytes, io.IOBase],
    bucket: str,
    key: str,
    content_type: str = "application/octet-stream",
    metadata: Optional[dict] = None,
    storage_class: str = "STANDARD",
    acl: Optional[str] = None,
    config: Optional[StorageConfig] = None,
) -> UploadResponse:
    s3_client = get_s3_client(config)

    put_kwargs = {
        "Bucket": bucket,
        "Key": key,
        "ContentType": content_type,
        "StorageClass": storage_class,
    }

    if metadata:
        put_kwargs["Metadata"] = metadata

    if acl:
        put_kwargs["ACL"] = acl

    try:
        if isinstance(source, str) and os.path.isfile(source):
            s3_client.upload_file(
                Filename=source,
                Bucket=bucket,
                Key=key,
                ExtraArgs={
                    k: v for k, v in put_kwargs.items() if k not in ("Bucket", "Key")
                },
            )
            head = s3_client.head_object(Bucket=bucket, Key=key)
            return UploadResponse(
                success=True,
                key=key,
                bucket=bucket,
                etag=head.get("ETag", "").strip('"'),
                version_id=head.get("VersionId"),
                content_length=head.get("ContentLength", 0),
            )

        if isinstance(source, bytes):
            put_kwargs["Body"] = source
        elif isinstance(source, io.IOBase):
            put_kwargs["Body"] = source
        else:
            put_kwargs["Body"] = source

        response = s3_client.put_object(**put_kwargs)

        return UploadResponse(
            success=True,
            key=key,
            bucket=bucket,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=len(source) if isinstance(source, bytes) else 0,
        )

    except ClientError as e:
        return UploadResponse(
            success=False,
            key=key,
            bucket=bucket,
            error=handle_aws_error(e, "upload_object"),
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            key=key,
            bucket=bucket,
            error=f"upload_object error: {str(e)}",
        )


def upload_object_from_request(
    request: UploadRequest,
    source: Union[str, bytes, io.IOBase],
    config: Optional[StorageConfig] = None,
) -> UploadResponse:
    return upload_object(
        source=source,
        bucket=request.bucket,
        key=request.key,
        content_type=request.content_type,
        metadata=request.metadata,
        storage_class=request.storage_class,
        acl=request.acl,
        config=config,
    )
