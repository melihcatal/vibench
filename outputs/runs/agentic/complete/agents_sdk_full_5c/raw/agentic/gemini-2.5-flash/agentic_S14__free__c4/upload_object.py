import os
import mimetypes
from storage_client import get_s3_client
from storage_models import ObjectUploadRequest, ObjectUploadResponse

def upload_object(
    request: ObjectUploadRequest
) -> ObjectUploadResponse:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.
    """
    s3_client = get_s3_client()

    if request.file_path and not os.path.exists(request.file_path):
        return ObjectUploadResponse(success=False, message=f"File not found at {request.file_path}")

    try:
        extra_args = {}
        if request.content_type:
            extra_args["ContentType"] = request.content_type
        elif request.file_path:
            mime_type, _ = mimetypes.guess_type(request.file_path)
            if mime_type:
                extra_args["ContentType"] = mime_type

        if request.file_path:
            with open(request.file_path, "rb") as f:
                response = s3_client.put_object(
                    Bucket=request.bucket_name,
                    Key=request.object_key,
                    Body=f,
                    **extra_args
                )
        elif request.data_bytes is not None:
            response = s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_key,
                Body=request.data_bytes,
                **extra_args
            )
        else:
            return ObjectUploadResponse(success=False, message="Either file_path or data_bytes must be provided.")

        etag = response.get("ETag", "").strip('"')
        version_id = response.get("VersionId")

        return ObjectUploadResponse(
            success=True,
            message="Object uploaded successfully",
            etag=etag,
            version_id=version_id
        )
    except Exception as e:
        return ObjectUploadResponse(success=False, message=f"Error uploading object: {str(e)}")
