from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_name
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ObjectSummary,
    parse_s3_datetime,
)


def list_objects_by_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    validate_bucket_name(request.bucket)

    list_kwargs = {
        "Bucket": request.bucket,
        "Prefix": request.prefix,
        "MaxKeys": request.max_keys,
    }

    if request.delimiter:
        list_kwargs["Delimiter"] = request.delimiter

    if request.start_after:
        list_kwargs["StartAfter"] = request.start_after

    all_objects = []
    all_prefixes = []
    is_truncated = False
    next_token = None

    try:
        response = s3_client.list_objects_v2(**list_kwargs)

        for obj in response.get("Contents", []):
            all_objects.append(
                ObjectSummary(
                    key=obj["Key"],
                    size=obj.get("Size"),
                    last_modified=parse_s3_datetime(obj.get("LastModified")),
                    etag=obj.get("ETag", "").strip('"'),
                    storage_class=obj.get("StorageClass"),
                )
            )

        for cp in response.get("CommonPrefixes", []):
            all_prefixes.append(cp["Prefix"])

        is_truncated = response.get("IsTruncated", False)
        if is_truncated:
            next_token = response.get("NextContinuationToken")

        return ListPrefixResponse(
            success=True,
            objects=all_objects,
            common_prefixes=all_prefixes,
            is_truncated=is_truncated,
            next_continuation_token=next_token,
        )
    except ClientError as e:
        return ListPrefixResponse(
            success=False,
            error=f"AWS S3 list_objects_v2 failed: {e.response['Error']['Code']} - {e.response['Error']['Message']}",
        )
    except Exception as e:
        return ListPrefixResponse(
            success=False,
            error=str(e),
        )
