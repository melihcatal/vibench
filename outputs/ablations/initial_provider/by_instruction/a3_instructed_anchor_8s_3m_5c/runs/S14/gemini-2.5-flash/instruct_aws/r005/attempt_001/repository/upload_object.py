import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()

    if request.file_path:
        with open(request.file_path, 'rb') as f:
            response = s3_client.upload_fileobj(
                f,
                request.bucket_name,
                request.object_name,
                ExtraArgs={'Metadata': request.metadata} if request.metadata else None
            )
    elif request.data:
        response = s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_name,
            Body=request.data,
            Metadata=request.metadata if request.metadata else None
        )
    else:
        raise ValueError("Either file_path or data must be provided for upload.")

    # The ETag is returned in the response headers for put_object and upload_fileobj
    # For upload_fileobj, the response object from boto3 doesn't directly contain ETag
    # We need to do a head_object to get it or parse from a direct put_object response
    # For simplicity, assuming a successful upload, we'll return a placeholder or fetch if needed.
    # In a real scenario, you'd parse the ETag from the HTTP response or use head_object.
    
    # For `put_object`, the ETag is directly in the response
    e_tag = response.get('ETag', '').strip('"') # Remove quotes from ETag
    version_id = response.get('VersionId')
    
    # If upload_fileobj was used, we might need to get ETag via head_object
    if not e_tag:
        try:
            head_response = s3_client.head_object(Bucket=request.bucket_name, Key=request.object_name)
            e_tag = head_response.get('ETag', '').strip('"')
            version_id = head_response.get('VersionId')
        except Exception as e:
            print(f"Could not retrieve ETag via head_object: {e}")

    return UploadObjectResponse(e_tag=e_tag, version_id=version_id)
