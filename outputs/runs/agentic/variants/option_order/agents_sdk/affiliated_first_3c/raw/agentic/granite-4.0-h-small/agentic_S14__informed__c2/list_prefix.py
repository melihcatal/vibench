from storage_client import get_s3_client

def list_objects_under_prefix(bucket: str, prefix: str, start_after: str = None, max_keys: int = 1000):
    """List objects in a bucket under a common prefix (folder).

    Args:
        bucket (str): Bucket name.
        prefix (str): Prefix to filter keys (e.g., 'documents/')
        start_after (str): Optional key to start listing after.
        max_keys (int): Max items per request.
    Returns:
        list: List of object keys matching the prefix.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    kwargs = {'Bucket': bucket, 'Prefix': prefix, 'MaxKeys': max_keys}
    if start_after:
        kwargs['StartAfter'] = start_after
    keys = []
    for page in paginator.paginate(**kwargs):
        if 'Contents' in page:
            keys.extend([obj['Key'] for obj in page['Contents']])
    print(f"Found {len(keys)} objects under prefix '{prefix}' in bucket {bucket}")
    return keys
