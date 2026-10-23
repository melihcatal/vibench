from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(
    request: ListPrefixRequest,
) -> ListPrefixResponse:
    """Lists stored objects under an AWS S3 bucket prefix."""
    s3_client = get_s3_client()

    object_keys = []
    common_prefixes = []

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(
        Bucket=request.bucket_name,
        Prefix=request.prefix,
        MaxKeys=request.max_keys,
        Delimiter='/'
    )

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                object_keys.append(obj['Key'])
        if 'CommonPrefixes' in page:
            for common_prefix in page['CommonPrefixes']:
                common_prefixes.append(common_prefix['Prefix'])

    return ListPrefixResponse(
        prefix=request.prefix,
        object_keys=object_keys,
        common_prefixes=common_prefixes,
    )
