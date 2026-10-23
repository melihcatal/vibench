from storage_client import get_storage_client
from storage_models import UploadRequest


def upload_object(request: UploadRequest):
    """
    Uploads a file or byte stream to an S3 bucket.
    """
    s3_client = get_storage_client()

    if request.file_path:
        s3_client.upload_file(
            request.file_path, request.storage_object.bucket, request.storage_object.key
        )
    elif request.file_content:
        s3_client.put_object(
            Bucket=request.storage_object.bucket,
            Key=request.storage_object.key,
            Body=request.file_content,
        )
    else:
        raise ValueError("Either file_path or file_content must be provided.")

    return {
        "status": "success",
        "bucket": request.storage_object.bucket,
        "key": request.storage_object.key,
    }
