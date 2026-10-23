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
        objects = []
        continuation_token = None

        while True:
            list_kwargs = {
                "Bucket": request.bucket,
                "Prefix": request.prefix or "",
                "MaxKeys": request.max_keys or 1000,
            }

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)

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

            if not response.get("IsTruncated"):
                break

            continuation_token = response.get("NextContinuationToken")

        return ListResponse(
            success=True,
            objects=objects,
            bucket=request.bucket,
            prefix=request.prefix or "",
            count=len(objects),
            message=f"Listed {len(objects)} objects from s3://{request.bucket}/{request.prefix or ''}",
        )

    except ClientError as e:
        return ListResponse(
            success=False,
            objects=[],
            bucket=request.bucket,
            prefix=request.prefix or "",
            error_message=str(e),
            message=f"Failed to list objects from AWS S3: {e}",
        )
