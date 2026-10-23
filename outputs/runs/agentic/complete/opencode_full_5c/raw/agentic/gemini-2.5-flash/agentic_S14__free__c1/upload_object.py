from storage_client import get_storage_client
from storage_models import UploadObjectRequest


def upload_object(request: UploadObjectRequest):
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)
    blob.upload_from_string(request.data, content_type=request.content_type)
    return {
        "message": f"Object {request.object_name} uploaded to {request.bucket_name}."
    }
