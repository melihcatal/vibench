from typing import BinaryIO, Optional, Union

from storage_client import get_bucket_name, get_s3_client, make_object_key, optional_content_type
from storage_models import StorageObjectRequest, StorageObjectResponse


def upload_object(
    bucket: Optional[str],
    object_key: str,
    body: Union[bytes, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> StorageObjectResponse:
    client = get_s3_client()
    bucket_name = bucket or get_bucket_name()
    key = make_object_key(object_key)
    request = StorageObjectRequest(bucket=bucket_name, object_key=key, content_type=content_type, metadata=metadata)
    kwargs = {'Bucket': request.bucket, 'Key': request.object_key, 'Body': body}
    if request.content_type:
        kwargs['ContentType'] = optional_content_type(request.content_type)
    if request.metadata:
        kwargs['Metadata'] = dict(request.metadata)
    response = client.put_object(**kwargs)
    return StorageObjectResponse(bucket=request.bucket, object_key=request.object_key, etag=response.get('ETag'), version_id=response.get('VersionId'))
