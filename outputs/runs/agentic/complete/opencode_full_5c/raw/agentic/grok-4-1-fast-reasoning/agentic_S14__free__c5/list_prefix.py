from storage_client import create_aws_client
from storage_models import ListObjectsResponse, ObjectInfo


def list_objects_prefix(bucket: str, prefix: str = "") -> ListObjectsResponse:
    client = create_aws_client("s3")
    paginator = client.get_paginator("list_objects_v2")
    objects: ListObjectsResponse = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if "Contents" in page:
            for obj in page["Contents"]:
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "etag": obj["ETag"].strip('"'),
                    }
                )
    return objects
