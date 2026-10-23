from storage_client import get_gcs_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = get_gcs_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if request.content_type:
        blob.upload_from_string(request.data, content_type=request.content_type)
    else:
        blob.upload_from_string(request.data)

    blob.reload()
    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=blob.size,
        e_tag=blob.etag,
        self_link=blob.self_link,
    )
