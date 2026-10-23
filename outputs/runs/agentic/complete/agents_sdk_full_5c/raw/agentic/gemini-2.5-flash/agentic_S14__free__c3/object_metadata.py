import os
import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata or None:
    """
    Retrieves metadata for an S3 object.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The object key for which to retrieve metadata.

    Returns:
        ObjectMetadata or None: An ObjectMetadata object if successful, None otherwise.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        print(f"Retrieved metadata for s3://{bucket_name}/{object_key}")
        return ObjectMetadata(
            key=object_key,
            last_modified=response.get('LastModified'),
            size=response.get('ContentLength'),
            content_type=response.get('ContentType'),
            e_tag=response.get('ETag'),
            storage_class=response.get('StorageClass'),
            user_metadata=response.get('Metadata', {})
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Object s3://{bucket_name}/{object_key} not found.")
        else:
            print(f"Error retrieving object metadata: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and key)
    # Ensure AWS credentials are configured
    _bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-aws-s3-bucket-name")
    _object_key = "example-uploads/test_upload.txt" # Use an existing object

    metadata = get_object_metadata(_bucket_name, _object_key)
    if metadata:
        print(f"\nObject Key: {metadata.key}")
        print(f"Last Modified: {metadata.last_modified}")
        print(f"Size: {metadata.size} bytes")
        print(f"Content Type: {metadata.content_type}")
        print(f"Etag: {metadata.e_tag}")
        print(f"Storage Class: {metadata.storage_class}")
        print(f"User Metadata: {metadata.user_metadata}")
    else:
        print("Failed to retrieve object metadata.")
