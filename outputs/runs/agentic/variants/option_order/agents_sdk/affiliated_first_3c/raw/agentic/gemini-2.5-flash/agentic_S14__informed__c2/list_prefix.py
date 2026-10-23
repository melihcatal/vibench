
from storage_client import get_s3_client
from storage_models import ListObjectsRequest, ListObjectsResponse

def list_objects_with_prefix(request: ListObjectsRequest) -> ListObjectsResponse:
    s3_client = get_s3_client()

    list_params = {
        'Bucket': request.bucket_name,
        'Delimiter': '/'
    }
    if request.prefix:
        list_params['Prefix'] = request.prefix
    if request.max_keys:
        list_params['MaxKeys'] = request.max_keys

    response = s3_client.list_objects_v2(**list_params)

    object_keys = [content['Key'] for content in response.get('Contents', [])]
    common_prefixes = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]

    return ListObjectsResponse(object_keys=object_keys, common_prefixes=common_prefixes)
