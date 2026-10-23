import os
import io
from storage_client import get_s3_client, S3_BUCKET_NAME
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    
    try:
        if isinstance(request.data, bytes):
            data_stream = io.BytesIO(request.data)
        elif isinstance(request.data, io.BytesIO):
            data_stream = request.data
        else:
            raise ValueError("Data must be bytes or io.BytesIO")

        s3_client.upload_fileobj(
            data_stream,
            S3_BUCKET_NAME,
            request.object_key,
            ExtraArgs=request.metadata
        )
        return UploadObjectResponse(success=True, object_key=request.object_key)
    except Exception as e:
        return UploadObjectResponse(success=False, error_message=str(e))
