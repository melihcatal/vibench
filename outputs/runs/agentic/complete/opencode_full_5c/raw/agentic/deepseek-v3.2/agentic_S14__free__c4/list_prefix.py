import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from storage_client import get_s3_client
from storage_models import ListObjectsRequest, ListObjectsResponse, S3Object


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000, delimiter: str = None
) -> ListObjectsResponse:
    """
    Lists stored objects under a bucket or container prefix in AWS S3.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (optional)
        max_keys: Maximum number of objects to return (default: 1000)
        delimiter: Character to group keys by (e.g., '/' for directory-like structure)

    Returns:
        ListObjectsResponse with list of objects and prefixes
    """
    s3_client = get_s3_client()

    try:
        # Prepare parameters for list_objects_v2
        params = {"Bucket": bucket_name, "MaxKeys": max_keys}

        if prefix:
            params["Prefix"] = prefix

        if delimiter:
            params["Delimiter"] = delimiter

        # List objects
        response = s3_client.list_objects_v2(**params)

        # Extract objects
        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                s3_obj = S3Object(
                    key=obj["Key"],
                    size=obj.get("Size", 0),
                    last_modified=obj["LastModified"].isoformat()
                    if hasattr(obj["LastModified"], "isoformat")
                    else str(obj["LastModified"]),
                    etag=obj.get("ETag", ""),
                    storage_class=obj.get("StorageClass", "STANDARD"),
                )
                objects.append(s3_obj)

        # Extract common prefixes (when delimiter is used)
        common_prefixes = []
        if "CommonPrefixes" in response:
            for prefix_obj in response["CommonPrefixes"]:
                common_prefixes.append(prefix_obj["Prefix"])

        # Check if there are more objects to list
        is_truncated = response.get("IsTruncated", False)
        continuation_token = response.get("NextContinuationToken")

        return ListObjectsResponse(
            success=True,
            bucket=bucket_name,
            prefix=prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=is_truncated,
            continuation_token=continuation_token,
            max_keys=max_keys,
            key_count=len(objects),
            provider="aws_s3",
        )

    except ClientError as e:
        return ListObjectsResponse(
            success=False, error_message=str(e), provider="aws_s3"
        )
    except Exception as e:
        return ListObjectsResponse(
            success=False, error_message=str(e), provider="aws_s3"
        )


def list_all_objects_with_prefix(bucket_name: str, prefix: str = "") -> List[S3Object]:
    """
    Lists all objects under a prefix, handling pagination automatically.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (optional)

    Returns:
        List of all S3Object instances under the prefix
    """
    s3_client = get_s3_client()
    all_objects = []
    continuation_token = None

    try:
        while True:
            params = {"Bucket": bucket_name, "Prefix": prefix}

            if continuation_token:
                params["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**params)

            if "Contents" in response:
                for obj in response["Contents"]:
                    s3_obj = S3Object(
                        key=obj["Key"],
                        size=obj.get("Size", 0),
                        last_modified=obj["LastModified"].isoformat()
                        if hasattr(obj["LastModified"], "isoformat")
                        else str(obj["LastModified"]),
                        etag=obj.get("ETag", ""),
                        storage_class=obj.get("StorageClass", "STANDARD"),
                    )
                    all_objects.append(s3_obj)

            if not response.get("IsTruncated", False):
                break

            continuation_token = response.get("NextContinuationToken")

    except ClientError as e:
        print(f"Error listing objects: {e}")

    return all_objects


if __name__ == "__main__":
    # Example usage
    request = ListObjectsRequest(
        bucket="my-example-bucket", prefix="test/", max_keys=100
    )
    result = list_objects_with_prefix(request.bucket, request.prefix, request.max_keys)
    print(f"List objects result: {result.success}")
    if result.success:
        print(f"Found {result.key_count} objects")
        for obj in result.objects[:5]:  # Show first 5 objects
            print(f"  - {obj.key} ({obj.size} bytes)")
