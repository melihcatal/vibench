import os
from typing import Union, BinaryIO
from storage_client import StorageClient
from storage_models import UploadObjectResponse

def upload_object(
    bucket_name: str,
    object_name: str,
    file_content: Union[str, bytes, BinaryIO],
    content_type: str = 'application/octet-stream',
    metadata: dict = None
) -> UploadObjectResponse:
    """Uploads a file or byte stream to AWS S3.

    Args:
        bucket_name: The name of the S3 bucket.
        object_name: The name of the object to create in the bucket.
        file_content: The content to upload. Can be a string, bytes, or a file-like object.
        content_type: The content type of the object.
        metadata: A dictionary of metadata to associate with the object.

    Returns:
        An UploadObjectResponse containing the ETag and VersionId of the uploaded object.
    """
    s3_client = StorageClient.get_client()

    extra_args = {'ContentType': content_type}
    if metadata:
        extra_args['Metadata'] = metadata

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=file_content,
        **extra_args
    )

    return UploadObjectResponse(
        etag=response.get('ETag', '').strip('\"\'),
        version_id=response.get('VersionId')
    )
