import os
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class RecordExportArchiveError(Exception):
    pass


def archive_record_export(
    source_path: str,
    bucket_name: str,
    object_key: str,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> str:
    if not source_path:
        raise RecordExportArchiveError("source_path is required")
    if not bucket_name:
        raise RecordExportArchiveError("bucket_name is required")
    if not object_key:
        raise RecordExportArchiveError("object_key is required")

    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = {str(k): str(v) for k, v in metadata.items()}

    try:
        if extra_args:
            s3.upload_file(source_path, bucket_name, object_key, ExtraArgs=extra_args)
        else:
            s3.upload_file(source_path, bucket_name, object_key)
    except (ClientError, BotoCoreError, OSError) as exc:
        raise RecordExportArchiveError(str(exc)) from exc

    return f"s3://{bucket_name}/{object_key}"
