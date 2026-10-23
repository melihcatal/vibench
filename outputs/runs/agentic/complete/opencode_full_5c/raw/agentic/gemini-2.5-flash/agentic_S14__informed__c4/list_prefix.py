import logging
from typing import Optional
from storage_client import get_s3_client
from storage_models import ListObjectsResponse, ObjectSummary

logger = logging.getLogger(__name__)


def list_objects_with_prefix(
    bucket_name: str,
    prefix: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
) -> ListObjectsResponse:
    s3_client = get_s3_client()
    try:
        list_kwargs = {"Bucket": bucket_name, "Prefix": prefix, "MaxKeys": max_keys}
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**list_kwargs)

        objects = []
        if "Contents" in response:
            for obj in response["Contents"]:
                objects.append(
                    ObjectSummary(
                        key=obj["Key"],
                        last_modified=obj["LastModified"].isoformat(),
                        e_tag=obj["ETag"].strip('"'),
                        size=obj["Size"],
                    )
                )

        next_token = response.get("NextContinuationToken")
        return ListObjectsResponse(objects=objects, next_continuation_token=next_token)
    except Exception as e:
        logger.error(
            f"Error listing objects with prefix '{prefix}' in bucket {bucket_name}: {e}"
        )
        raise
