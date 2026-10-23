from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary
from botocore.exceptions import ClientError


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    try:
        # The AWS S3 client lists objects within a bucket that match a given prefix.
        # This is useful for hierarchical organization of objects.
        response = s3_client.list_objects_v2(
            Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
        )

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    ObjectSummary(
                        key=obj["Key"],
                        last_modified=obj["LastModified"].isoformat()
                        if obj.get("LastModified")
                        else None,
                        etag=obj["ETag"],
                        size=obj["Size"],
                    )
                )

        next_continuation_token = response.get("NextContinuationToken")

        return ListPrefixResponse(
            success=True,
            message="Objects listed successfully",
            objects=objects,
            next_continuation_token=next_continuation_token,
        )
    except ClientError as e:
        return ListPrefixResponse(success=False, message=f"AWS S3 ClientError: {e}")
    except Exception as e:
        return ListPrefixResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
