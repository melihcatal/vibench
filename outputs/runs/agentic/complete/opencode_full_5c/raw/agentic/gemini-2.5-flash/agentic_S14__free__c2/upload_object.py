from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    response = s3_client.put_object(
        Bucket=request.bucket_name,
        Key=request.object_key,
        Body=request.file_content,
        ContentType=request.content_type if request.content_type else 'application/octet-stream'
    )
    return UploadObjectResponse(
        e_tag=response['ETag'].strip('\"\'),
        version_id=response.get('VersionId')
    )
