import os
from typing import Union
from io import BytesIO

from botocore.exceptions import ClientError
from storage_client import get_storage_client

def upload_file_to_s3(
    bucket_name: str,
    object_key: str,
    file_source: Union[str, BytesIO]
) -> bool:
    """
    Uploads a file or a byte stream to an S3 bucket.

    Args:
        bucket_name: The name of the target S3 bucket.
        object_key: The desired key (path) for the object in the bucket.
        file_source: The local file path (str) or a file-like object (BytesIO).

    Returns:
        True if the upload was successful, False otherwise.
    """
    s3_client = get_storage_client()
    try:
        if isinstance(file_source, str):
            s3_client.upload_file(file_source, bucket_name, object_key)
        elif isinstance(file_source, BytesIO):
            s3_client.upload_fileobj(file_source, bucket_name, object_key)
        else:
            raise TypeError("file_source must be a file path (str) or BytesIO object.")
        print(f"Successfully uploaded to s3://{bucket_name}/{object_key}")
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: The file was not found at path: {file_source}")
        return False

# Example usage (requires environment variables to be set)
# if __name__ == '__main__':
#     BUCKET = os.environ.get("AWS_S3_BUCKET")
#     if BUCKET:
#         # Create a dummy file in memory
#         dummy_content = b"This is a test file for S3 upload."
#         dummy_file = BytesIO(dummy_content)
#         upload_file_to_s3(BUCKET, "test-upload.txt", dummy_file)
#     else:
#         print("AWS_S3_BUCKET environment variable not set.")
