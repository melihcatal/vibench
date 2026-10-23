
from storage_client import get_s3_client
from storage_models import ObjectStorageUploadRequest, ObjectStorageUploadResponse

def upload_object(request: ObjectStorageUploadRequest) -> ObjectStorageUploadResponse:
    s3_client = get_s3_client()
    upload_params = {
        'Bucket': request.bucket_name,
        'Key': request.object_key,
        'Body': request.data
    }
    if request.content_type:
        upload_params['ContentType'] = request.content_type

    response = s3_client.put_object(**upload_params)

    return ObjectStorageUploadResponse(
        e_tag=response.get('ETag', '').strip('\"\'),
        version_id=response.get('VersionId')
    )
