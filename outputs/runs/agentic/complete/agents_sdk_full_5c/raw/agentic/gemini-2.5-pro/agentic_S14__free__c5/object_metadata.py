import os
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ObjectMetadata

def get_s3_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata | None:
    """
    Retrieves metadata for an object stored in S3 without downloading it.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object.

    Returns:
        An ObjectMetadata object, or None if an error occurred or the object was not found.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        
        # Manually construct the Pydantic model
        metadata = ObjectMetadata(
            key=object_key,
            content_length=response.get('ContentLength'),
            content_type=response.get('ContentType'),
            last_modified=response.get('LastModified'),
            etag=response.get('ETag', '').strip('"'), # ETag often has quotes
            metadata=response.get('Metadata'),
            version_id=response.get('VersionId'),
        )
        return metadata

    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Object not found: s3://{bucket_name}/{object_key}")
        else:
            print(f"Error retrieving metadata for s3://{bucket_name}/{object_key}: {e}")
        return None

# Example usage
# if __name__ == '__main__':
#     BUCKET = os.environ.get("AWS_S3_BUCKET")
#     OBJECT_KEY = "test-upload.txt" # Assuming this object exists
#     if BUCKET:
#         metadata = get_s3_object_metadata(BUCKET, OBJECT_KEY)
#         if metadata:
#             print("Retrieved Object Metadata:")
#             print(metadata.model_dump_json(indent=2))
#     else:
#         print("AWS_S3_BUCKET environment variable not set.")
