from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectInfo


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    try:
        # Use paginator for potentially large number of objects
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=request.bucket_name, Prefix=request.prefix)

        objects = []
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append(
                        ObjectInfo(
                            key=obj["Key"],
                            last_modified=obj["LastModified"],
                            size=obj["Size"],
                            etag=obj["ETag"],
                        )
                    )
        return ListPrefixResponse(
            success=True,
            objects=objects,
            message=f"Listed objects under prefix {request.prefix} in bucket {request.bucket_name}.",
        )
    except Exception as e:
        return ListPrefixResponse(
            success=False,
            objects=[],
            message=f"Failed to list objects under prefix {request.prefix}: {str(e)}",
        )
