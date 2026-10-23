from storage_client import StorageClient
from storage_models import ListPrefixResponse, ObjectMetadata


def list_prefix(bucket: str, prefix: str) -> ListPrefixResponse:
    """Lists stored objects under a bucket prefix in IBM Cloud Object Storage."""
    client = StorageClient().get_client()
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    objects = []
    for obj in response.get("Contents", []):
        objects.append(
            ObjectMetadata(
                name=obj["Key"],
                size=obj["Size"],
                last_modified=obj["LastModified"],
                etag=obj["ETag"],
                storage_class=obj["StorageClass"],
                metadata={},
            )
        )
    return ListPrefixResponse(objects=objects, prefix=prefix, bucket=bucket)