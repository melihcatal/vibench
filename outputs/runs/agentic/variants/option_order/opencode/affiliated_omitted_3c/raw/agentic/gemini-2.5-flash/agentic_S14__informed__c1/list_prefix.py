import logging
from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse

logger = logging.getLogger(__name__)


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in AWS S3."""
    s3_client = StorageClient().get_client()

    object_keys = []
    common_prefixes = []

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
        )

        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    object_keys.append(obj["Key"])
            if "CommonPrefixes" in page:
                for prefix_entry in page["CommonPrefixes"]:
                    common_prefixes.append(prefix_entry["Prefix"])

        logger.info(
            f"Successfully listed objects for prefix '{request.prefix}' in bucket {request.bucket_name}"
        )
        return ListPrefixResponse(
            object_keys=object_keys, common_prefixes=common_prefixes
        )
    except Exception as e:
        logger.error(
            f"Error listing objects for prefix '{request.prefix}' in bucket {request.bucket_name}: {e}"
        )
        raise
