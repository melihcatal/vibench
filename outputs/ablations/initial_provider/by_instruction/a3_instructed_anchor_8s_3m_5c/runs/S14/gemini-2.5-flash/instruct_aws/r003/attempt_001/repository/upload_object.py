import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    if request.file_path:
        with open(request.file_path, "rb") as f:
            response = s3_client.upload_fileobj(
                f,
                request.bucket_name,
                request.object_key,
                ExtraArgs={'ContentType': request.content_type} if request.content_type else {}
            )
    elif request.data:
        response = s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_key,
            Body=request.data,
            ContentType=request.content_type if request.content_type else 'application/octet-stream'
        )
    else:
        raise ValueError("Either file_path or data must be provided in the request.")
    
    return UploadObjectResponse(
        e_tag=response['ETag'].strip('"'),
        version_id=response.get('VersionId')
    )
