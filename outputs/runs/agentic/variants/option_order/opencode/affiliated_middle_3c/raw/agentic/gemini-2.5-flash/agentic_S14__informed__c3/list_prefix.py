from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.list_objects_v2(
            Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
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

        message = f"Successfully listed {len(objects)} objects with prefix '{request.prefix}' in bucket '{request.bucket_name}'."
        return ListPrefixResponse(success=True, message=message, objects=objects)
    except Exception as e:
        return ListPrefixResponse(
            success=False, message=f"Error listing objects with prefix: {str(e)}"
        )
