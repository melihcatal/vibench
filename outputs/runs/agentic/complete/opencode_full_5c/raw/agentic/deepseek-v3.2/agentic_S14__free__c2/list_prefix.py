import boto3
from botocore.exceptions import ClientError
from typing import List, Dict
from storage_client import get_s3_client
from storage_models import ListRequest, ListResponse, ObjectInfo


def list_objects_with_prefix(request: ListRequest) -> ListResponse:
    """List stored objects under a bucket or container prefix in AWS S3."""
    s3_client = get_s3_client()

    try:
        objects: List[ObjectInfo] = []
        continuation_token = None

        while True:
            list_kwargs = {
                "Bucket": request.bucket,
                "Prefix": request.prefix if request.prefix else "",
                "MaxKeys": request.max_keys if request.max_keys else 1000,
            }

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)

            if "Contents" in response:
                for obj in response["Contents"]:
                    objects.append(
                        ObjectInfo(
                            key=obj["Key"],
                            size=obj.get("Size", 0),
                            last_modified=obj.get("LastModified"),
                            etag=obj.get("ETag", "").strip('"'),
                            storage_class=obj.get("StorageClass", "STANDARD"),
                        )
                    )

            # Check if there are more objects to fetch
            if response.get("IsTruncated"):
                continuation_token = response.get("NextContinuationToken")
            else:
                break

        return ListResponse(
            success=True,
            bucket=request.bucket,
            prefix=request.prefix,
            objects=objects,
            total_count=len(objects),
            message=f"Listed {len(objects)} objects from AWS S3 bucket '{request.bucket}' with prefix '{request.prefix}'",
        )

    except ClientError as e:
        return ListResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=str(e),
            message=f"Failed to list objects from AWS S3: {e.response['Error']['Code']}",
        )
    except Exception as e:
        return ListResponse(
            success=False,
            bucket=request.bucket,
            prefix=request.prefix,
            error_message=str(e),
            message=f"Failed to list objects: {str(e)}",
        )
