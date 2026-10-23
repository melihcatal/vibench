import os
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    try:
        if request.file_path:
            with open(request.file_path, "rb") as f:
                s3_client.upload_fileobj(
                    f,
                    request.bucket_name,
                    request.object_name,
                    ExtraArgs={"Metadata": request.metadata}
                    if request.metadata
                    else {},
                )
        elif request.data:
            s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_name,
                Body=request.data,
                Metadata=request.metadata if request.metadata else {},
            )
        else:
            return UploadObjectResponse(
                success=False, message="No file path or data provided for upload."
            )

        head_object_response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_name
        )
        etag = head_object_response.get("ETag")
        return UploadObjectResponse(
            success=True,
            message=f"Object {request.object_name} uploaded successfully to {request.bucket_name}.",
            etag=etag,
        )
    except Exception as e:
        return UploadObjectResponse(
            success=False, message=f"Error uploading object: {str(e)}"
        )
