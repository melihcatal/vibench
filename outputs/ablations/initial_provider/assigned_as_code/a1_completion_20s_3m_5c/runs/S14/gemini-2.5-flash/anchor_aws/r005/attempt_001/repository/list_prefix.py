import os
from storage_client import get_s3_client


def list_objects_with_prefix(payload, config=None):
    config = config or {}
    bucket_name = config.get("bucket", os.environ.get("AWS_S3_BUCKET_NAME"))
    prefix = payload.get("prefix", "")
    max_keys = payload.get("max_keys", 1000)  # Default max keys

    s3_client = get_s3_client(config.get("region"))

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append({
                    "object_name": obj["Key"],
                    "last_modified": obj["LastModified"].isoformat(),
                    "etag": obj["ETag"],
                    "size": obj["Size"],
                    "storage_class": obj["StorageClass"]
                })
        return {"objects": objects, "is_truncated": response.get("IsTruncated", False)}
    except Exception as e:
        raise RuntimeError(f"Error listing objects with prefix: {e}")
