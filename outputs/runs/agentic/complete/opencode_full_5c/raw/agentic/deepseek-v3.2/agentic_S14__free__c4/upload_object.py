import boto3
from botocore.exceptions import ClientError
import os
from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket_name: str,
    object_key: str,
    file_path: str = None,
    data: bytes = None,
    content_type: str = "application/octet-stream",
) -> UploadResponse:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket
        file_path: Path to local file to upload (optional if data is provided)
        data: Byte data to upload (optional if file_path is provided)
        content_type: MIME type of the object

    Returns:
        UploadResponse with upload details
    """
    s3_client = get_s3_client()

    try:
        extra_args = {"ContentType": content_type}

        if file_path:
            # Upload from file
            s3_client.upload_file(
                file_path, bucket_name, object_key, ExtraArgs=extra_args
            )
            file_size = os.path.getsize(file_path)
        elif data:
            # Upload from bytes
            s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data, ContentType=content_type
            )
            file_size = len(data)
        else:
            raise ValueError("Either file_path or data must be provided")

        # Get the object URL
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"

        return UploadResponse(
            success=True,
            bucket=bucket_name,
            key=object_key,
            url=object_url,
            size=file_size,
            content_type=content_type,
            provider="aws_s3",
        )

    except ClientError as e:
        return UploadResponse(success=False, error_message=str(e), provider="aws_s3")
    except Exception as e:
        return UploadResponse(success=False, error_message=str(e), provider="aws_s3")


if __name__ == "__main__":
    # Example usage
    request = UploadRequest(
        bucket="my-example-bucket", key="test/example.txt", file_path="/tmp/example.txt"
    )
    result = upload_object(request.bucket, request.key, file_path=request.file_path)
    print(f"Upload result: {result.success}")
    if result.success:
        print(f"Object URL: {result.url}")
        print(f"Size: {result.size} bytes")
