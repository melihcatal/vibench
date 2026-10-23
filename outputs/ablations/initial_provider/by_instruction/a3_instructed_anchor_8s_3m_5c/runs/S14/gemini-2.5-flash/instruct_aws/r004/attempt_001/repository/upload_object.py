import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()

    if request.file_path:
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"File not found at {request.file_path}")
        extra_args = {}
        s3_client.upload_file(request.file_path, request.bucket_name, request.object_name, ExtraArgs=extra_args)
        response = s3_client.head_object(Bucket=request.bucket_name, Key=request.object_name)
        return UploadObjectResponse(
            object_name=request.object_name,
            e_tag=response['ETag'].strip('\"'),
            version_id=response.get('VersionId')
        )
    elif request.data:
        response = s3_client.put_object(Bucket=request.bucket_name, Key=request.object_name, Body=request.data)
        return UploadObjectResponse(
            object_name=request.object_name,
            e_tag=response['ETag'].strip('\"'),
            version_id=response.get('VersionId')
        )
    else:
        raise ValueError("Either file_path or data must be provided for upload.")
