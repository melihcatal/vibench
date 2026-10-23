import os
import mimetypes
from typing import Union
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    try:
        extra_args = {}
        if request.content_type:
            extra_args["ContentType"] = request.content_type
        else:
            # Try to guess content type from file path if data is a string
            if isinstance(request.data, str) and os.path.exists(request.data):
                mime_type, _ = mimetypes.guess_type(request.data)
                if mime_type:
                    extra_args["ContentType"] = mime_type

        if isinstance(request.data, str) and os.path.exists(request.data):
            with open(request.data, "rb") as f:
                response = s3_client.upload_fileobj(
                    f, request.bucket_name, request.key, ExtraArgs=extra_args
                )
        elif isinstance(request.data, bytes):
            response = s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.key,
                Body=request.data,
                **extra_args,
            )
        else:
            raise ValueError("Data must be bytes or a valid file path string.")

        # S3 put_object and upload_fileobj don't always return VersionId directly
        # If versioning is enabled, it might be in the response headers.
        # For simplicity, we'll extract ETag which is always present.
        etag = response.get("ETag", "").strip("\"'")
        version_id = response.get("VersionId")

        return UploadObjectResponse(
            bucket_name=request.bucket_name,
            key=request.key,
            version_id=version_id,
            etag=etag,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to upload object {request.key} to {request.bucket_name}: {e}"
        )
