from datetime import datetime
from storage_client import StorageClient
from storage_models import ListPrefixResponse, ListedObject

def list_objects_with_prefix(bucket_name: str, prefix: str = '', delimiter: str = '') -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in AWS S3.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: The prefix to filter objects by. Objects whose names begin with this prefix will be listed.
        delimiter: A character used to group keys. If a delimiter is specified, common prefixes are returned.

    Returns:
        A ListPrefixResponse containing a list of objects and common prefixes.
    """
    s3_client = StorageClient.get_client()

    list_kwargs = {'Bucket': bucket_name}
    if prefix:
        list_kwargs['Prefix'] = prefix
    if delimiter:
        list_kwargs['Delimiter'] = delimiter

    response = s3_client.list_objects_v2(**list_kwargs)

    listed_objects = []
    if 'Contents' in response:
        for obj in response['Contents']:
            # AWS S3 returns 'LastModified' as a datetime object
            last_modified_dt = obj.get('LastModified')
            # Ensure last_modified is in a consistent string format, e.g., ISO 8601
            last_modified_str = last_modified_dt.isoformat() if isinstance(last_modified_dt, datetime) else str(last_modified_dt)
            listed_objects.append(ListedObject(
                object_name=obj.get('Key'),
                last_modified=last_modified_str,
                etag=obj.get('ETag', '').strip('\"\'),
                size=obj.get('Size')
            ))

    common_prefixes = [p.get('Prefix') for p in response.get('CommonPrefixes', [])]

    return ListPrefixResponse(objects=listed_objects, common_prefixes=common_prefixes)
