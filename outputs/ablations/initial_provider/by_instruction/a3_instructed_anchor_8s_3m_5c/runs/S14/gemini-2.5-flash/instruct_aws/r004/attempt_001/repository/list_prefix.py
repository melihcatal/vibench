from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListPrefixItem

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    try:
        params = {
            'Bucket': request.bucket_name,
            'Prefix': request.prefix
        }
        if request.delimiter:
            params['Delimiter'] = request.delimiter
        if request.max_keys:
            params['MaxKeys'] = request.max_keys

        response = s3_client.list_objects_v2(**params)

        contents = response.get('Contents', [])
        items = [
            ListPrefixItem(
                key=obj['Key'],
                last_modified=obj['LastModified'].isoformat(),
                size=obj['Size'],
                e_tag=obj['ETag'].strip('\"')
            )
            for obj in contents
        ]

        common_prefixes = [
            prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])
        ]

        return ListPrefixResponse(
            items=items,
            common_prefixes=common_prefixes
        )
    except Exception as e:
        raise RuntimeError(f"Error listing objects with prefix: {e}")
