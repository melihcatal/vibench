from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_prefix(
    bucket_name: str, prefix: str = None, max_keys: int = 1000
) -> ListPrefixResponse:
    """
    Lists stored objects under an Amazon S3 bucket prefix.
    """
    client = StorageClient().get_client()

    request: ListPrefixRequest = {
        "bucket_name": bucket_name,
        "prefix": prefix,
        "max_keys": max_keys,
    }

    try:
        response = client.list_objects_v2(
            Bucket=request["bucket_name"],
            Prefix=request["prefix"] or "",
            MaxKeys=request["max_keys"],
        )

        objects = []
        prefixes = []

        if "Contents" in response:
            objects = [obj["Key"] for obj in response["Contents"]]

        if "CommonPrefixes" in response:
            prefixes = [p["Prefix"] for p in response["CommonPrefixes"]]

        return {
            "objects": objects,
            "prefixes": prefixes,
            "is_truncated": response.get("IsTruncated", False),
            "next_marker": response.get("NextContinuationToken"),
        }
    except Exception as e:
        raise Exception(f"Failed to list objects in S3 bucket: {str(e)}")
