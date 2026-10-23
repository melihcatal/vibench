import os
from typing import List
import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary

def list_objects_under_prefix(
    request: ListPrefixRequest
) -> ListPrefixResponse:
    """
    Lists stored objects under a prefix in AWS S3 managed object storage.
    """
    s3_client = get_storage_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
            Prefix=request.prefix,
            MaxKeys=request.max_keys
        )

        objects: List[ObjectSummary] = []
        if "Contents" in response:
            objects = [
                ObjectSummary(
                    object_key=obj["Key"],
                    size=obj["Size"],
                    last_modified=obj["LastModified"],
                    etag=obj["ETag"]
                )
                for obj in response["Contents"]
            ]

        return ListPrefixResponse(
            prefix=request.prefix,
            objects=objects,
            success=True
        )
    except ClientError as e:
        return ListPrefixResponse(
            prefix=request.prefix,
            objects=[],
            success=False,
            error=str(e)
        )