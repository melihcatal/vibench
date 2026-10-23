from storage_client import get_s3_client
from storage_models import ListObjectsRequest, ListObjectsResponse

def list_objects_with_prefix(
    request: ListObjectsRequest
) -> ListObjectsResponse:
    """
    Lists stored objects under a bucket or container prefix in AWS S3.
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=request.bucket_name,
            Prefix=request.prefix,
            MaxKeys=request.max_keys
        )

        object_keys = [content["Key"] for content in response.get("Contents", [])]
        common_prefixes = [prefix["Prefix"] for prefix in response.get("CommonPrefixes", [])]

        return ListObjectsResponse(
            success=True,
            message="Objects listed successfully",
            object_keys=object_keys,
            common_prefixes=common_prefixes
        )
    except Exception as e:
        return ListObjectsResponse(success=False, message=f"Error listing objects: {str(e)}")
