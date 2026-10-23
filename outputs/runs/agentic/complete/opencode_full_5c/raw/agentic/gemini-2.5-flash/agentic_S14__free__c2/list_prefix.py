from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(
        Bucket=request.bucket_name,
        Prefix=request.prefix,
        MaxKeys=request.max_keys
    )
    objects = []
    for obj in response.get('Contents', []):
        objects.append(ListedObject(
            key=obj['Key'],
            last_modified=obj['LastModified'].isoformat(),
            e_tag=obj['ETag'].strip('\"\'),
            size=obj['Size']
        ))
    return ListPrefixResponse(objects=objects)
