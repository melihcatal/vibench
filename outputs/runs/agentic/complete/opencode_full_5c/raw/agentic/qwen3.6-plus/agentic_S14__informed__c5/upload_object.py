from storage_models import ObjectUploadRequest
from storage_client import get_storage_client, get_bucket, create_blob, upload_blob


def upload_object(bucket_name, object_name, content, content_type=None, metadata=None):
    request = ObjectUploadRequest(
        bucket=bucket_name,
        object_name=object_name,
        content=content,
        content_type=content_type,
        metadata=metadata,
    )
    client = get_storage_client()
    bucket = get_bucket(client, request.bucket)
    blob = create_blob(bucket, request.object_name)
    uploaded_blob = upload_blob(
        blob,
        request.content,
        content_type=request.content_type,
        metadata=request.metadata,
    )
    return {
        "bucket": uploaded_blob.bucket.name,
        "object_name": uploaded_blob.name,
        "size": uploaded_blob.size,
        "content_type": uploaded_blob.content_type,
        "etag": uploaded_blob.etag,
    }
