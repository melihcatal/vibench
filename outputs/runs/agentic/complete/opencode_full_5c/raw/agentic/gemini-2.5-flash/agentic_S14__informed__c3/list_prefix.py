from storage_client import get_s3_client
from typing import List


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> dict:
    """
    Lists stored objects under an Amazon S3 bucket prefix.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
        )
        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    {
                        "Key": obj["Key"],
                        "LastModified": obj["LastModified"].isoformat(),
                        "ETag": obj["ETag"],
                        "Size": obj["Size"],
                        "StorageClass": obj["StorageClass"],
                    }
                )
        return {"status": "success", "objects": objects}
    except Exception as e:
        return {"status": "error", "message": str(e)}
