import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ListRequest, ListResponse, ObjectInfo


def list_objects_with_prefix(request: ListRequest) -> ListResponse:
    """
    Lists stored objects under a bucket or container prefix in AWS S3.
    """
    s3_client = get_s3_client()

    try:
        # Build parameters for S3 list_objects_v2
        params = {"Bucket": request.bucket}

        if request.prefix:
            params["Prefix"] = request.prefix

        if request.max_keys:
            params["MaxKeys"] = request.max_keys

        if request.continuation_token:
            params["ContinuationToken"] = request.continuation_token

        # List objects from S3
        response = s3_client.list_objects_v2(**params)

        # Convert S3 objects to ObjectInfo models
        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    ObjectInfo(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        etag=obj["ETag"],
                        storage_class=obj.get("StorageClass", "STANDARD"),
                    )
                )

        # Get continuation token if there are more results
        next_token = response.get("NextContinuationToken")

        return ListResponse(
            success=True,
            bucket=request.bucket,
            prefix=request.prefix,
            objects=objects,
            next_continuation_token=next_token,
            is_truncated=response.get("IsTruncated", False),
            message=f"Listed {len(objects)} objects from s3://{request.bucket}/{request.prefix or ''}",
        )

    except ClientError as e:
        return ListResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=f"S3 list error: {str(e)}",
        )
    except Exception as e:
        return ListResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=f"List error: {str(e)}",
        )
