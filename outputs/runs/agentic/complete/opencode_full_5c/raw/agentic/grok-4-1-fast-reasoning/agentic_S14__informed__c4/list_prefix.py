import boto3
from typing import List
from storage_client import get_aws_client_kwargs
from storage_models import ListObjectsResult, ObjectMetadata


def list_prefix(
    bucket: str, prefix: str = "", delimiter: Optional[str] = None
) -> ListObjectsResult:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    objects: List[ObjectMetadata] = []
    common_prefixes: List[str] = []
    is_truncated = False
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter):
        if page.get("IsTruncated"):
            is_truncated = True
        if "CommonPrefixes" in page:
            common_prefixes.extend([cp["Prefix"] for cp in page["CommonPrefixes"]])
        if "Contents" in page:
            for obj in page["Contents"]:
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "etag": obj["ETag"].strip('"'),
                        "last_modified": obj["LastModified"].isoformat(),
                        "content_type": None,
                        "metadata": None,
                    }
                )
    return {
        "objects": objects,
        "is_truncated": is_truncated,
        "common_prefixes": common_prefixes,
    }
