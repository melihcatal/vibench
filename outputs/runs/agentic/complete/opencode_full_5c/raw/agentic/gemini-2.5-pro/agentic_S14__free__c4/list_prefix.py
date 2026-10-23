from typing import List
from storage_client import get_storage_client
from storage_models import ObjectMetadata


def list_objects_with_prefix(bucket: str, prefix: str) -> List[ObjectMetadata]:
    s3_client = get_storage_client()
    objects = []
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append(
                        ObjectMetadata(
                            key=obj["Key"],
                            size=obj.get("Size"),
                            last_modified=obj.get("LastModified").isoformat(),
                            etag=obj.get("ETag"),
                            version_id=None,
                            content_type=None,
                            metadata=None,
                        )
                    )
    except Exception as e:
        print(f"Error listing objects: {e}")
    return objects
