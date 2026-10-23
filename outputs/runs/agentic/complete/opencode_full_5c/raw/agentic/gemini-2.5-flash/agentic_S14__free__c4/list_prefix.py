from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject
from botocore.exceptions import ClientError


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = StorageClient().get_s3_client()
    try:
        response = s3_client.list_objects_v2(
            Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    ListedObject(
                        key=obj["Key"],
                        last_modified=obj["LastModified"].isoformat(),
                        etag=obj["ETag"].strip('"'),
                        size=obj["Size"],
                    )
                )

        return ListPrefixResponse(
            success=True, objects=objects, message="Objects listed successfully."
        )
    except ClientError as e:
        return ListPrefixResponse(
            success=False, objects=[], message=f"Error listing objects: {e}"
        )
