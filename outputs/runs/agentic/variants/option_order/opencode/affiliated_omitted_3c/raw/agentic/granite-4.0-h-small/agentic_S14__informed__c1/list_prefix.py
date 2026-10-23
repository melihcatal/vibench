import boto3
import os
from .storage_client import StorageClient
from .storage_models import ObjectMetadata


class ListPrefix:
    """List objects under a bucket or prefix using S3 ListObjectsV2."""

    @classmethod
    def list(cls, bucket_name: str, prefix: str = "", max_keys: int = 1000):
        paginator = StorageClient.s3.get_paginator("list_objects_v2")
        iterator = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix,
            PaginationConfig={"MaxItems": max_keys},
        )
        objects = []
        for page in iterator:
            contents = page.get("Contents", [])
            for obj in contents:
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"],
                        "storage_class": obj["StorageClass"],
                    }
                )
        return {
            "status": "listed",
            "bucket": bucket_name,
            "prefix": prefix,
            "objects": objects,
        }
