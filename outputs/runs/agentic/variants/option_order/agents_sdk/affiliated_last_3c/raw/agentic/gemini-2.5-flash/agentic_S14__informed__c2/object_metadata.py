import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def get_object_metadata(bucket_name: str, object_name: str) -> ObjectMetadata | None:
    """
    Retrieves metadata for a specific object in an S3 bucket.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        metadata = response.get('Metadata', {})
        content_type = response.get('ContentType')
        last_modified = response.get('LastModified')
        size = response.get('ContentLength')

        return ObjectMetadata(
            bucket_name=bucket_name,
            object_name=object_name,
            etag=response.get('ETag', '').strip('\"'),
            last_modified=last_modified.isoformat() if last_modified else None,
            size=size,
            content_type=content_type,
            user_metadata=metadata
        )
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Object {object_name} not found in bucket {bucket_name}")
        else:
            print(f"Error retrieving object metadata: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with actual values)
    bucket = os.environ.get("S3_BUCKET_NAME", "my-test-bucket")
    object_key = "test/example.txt"
    metadata = get_object_metadata(bucket, object_key)
    if metadata:
        print(f"Metadata for {object_key}:\n{metadata.model_dump_json(indent=2)}")
