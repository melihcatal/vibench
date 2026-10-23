import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ListRequest, ListResponse, S3Object


def list_objects_with_prefix(request: ListRequest) -> ListResponse:
    """List stored objects under a bucket or container prefix in AWS S3."""
    s3_client = get_s3_client()

    try:
        paginator = s3_client.get_paginator("list_objects_v2")

        # Prepare pagination parameters
        pagination_config = {"Bucket": request.bucket, "Prefix": request.prefix or ""}

        if request.max_keys:
            pagination_config["MaxKeys"] = request.max_keys

        objects = []
        common_prefixes = []

        # Paginate through results
        for page in paginator.paginate(**pagination_config):
            # Process objects
            for obj in page.get("Contents", []):
                objects.append(
                    S3Object(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        etag=obj["ETag"],
                        storage_class=obj.get("StorageClass", "STANDARD"),
                    )
                )

            # Process common prefixes (folders)
            for prefix in page.get("CommonPrefixes", []):
                common_prefixes.append(prefix["Prefix"])

        return ListResponse(
            success=True,
            objects=objects,
            common_prefixes=common_prefixes,
            bucket=request.bucket,
            prefix=request.prefix or "",
            message=f"Found {len(objects)} objects and {len(common_prefixes)} prefixes",
        )

    except ClientError as e:
        return ListResponse(success=False, error_message=f"AWS S3 error: {str(e)}")
    except Exception as e:
        return ListResponse(
            success=False, error_message=f"Failed to list objects: {str(e)}"
        )
