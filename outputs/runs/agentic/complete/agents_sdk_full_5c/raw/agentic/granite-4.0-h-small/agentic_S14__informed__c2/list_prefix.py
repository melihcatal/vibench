import os
from storage_client import create_aws_s3_client
from storage_models import S3ListResult

def list_prefix(bucket_name, prefix='', delimiter=None, max_keys=1000):
    """List objects under a bucket with the given prefix using S3 API.

    Uses AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for auth.
    Returns S3ListResult containing a list of S3 Summary objects, each with Key, Size, LastModified.
    """
    client = create_aws_s3_client()
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter=delimiter,
        PaginationConfig={'PageSize': max_keys}
    )
    items = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                items.append({'Key': obj['Key'], 'Size': obj['Size'], 'LastModified': obj['LastModified']})
        if 'CommonPrefixes' in page:
            for cp in page['CommonPrefixes']:
                items.append({'Key': cp['Prefix'], 'Size': None, 'LastModified': None})
    return S3ListResult(bucket=bucket_name, prefix=prefix, delimiter=delimiter, items=items)
