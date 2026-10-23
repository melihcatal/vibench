from storage_client import get_s3_client
from storage_models import StorageObject, UploadResponse
from typing import Union


def upload_object(
    storage_object: StorageObject, data: Union[bytes, str]
) -> UploadResponse:
    """
    Uploads a file or byte stream to Amazon S3.
    """
    s3_client = get_s3_client()
    if isinstance(data, str):
        data = data.encode("utf-8")

    response = s3_client.put_object(
        Bucket=storage_object.bucket_name,
        Key=storage_object.object_key,
        Body=data,
        ContentType=storage_object.content_type,
    )
    return UploadResponse(etag=response["ETag"], version_id=response.get("VersionId"))
