import boto3
from storage_client import get_s3_client
from typing import Dict, Any

def get_object_metadata(bucket_name: str, object_key: str) -> Dict[str, Any]:
    """
    Reads object metadata or head information from AWS S3 managed object storage.
    """
    s3_client = get_s3_client()
    
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        # The 'ResponseMetadata' is not typically part of the object metadata itself
        # We return relevant headers/metadata
        metadata = {
            'ContentLength': response.get('ContentLength'),
            'ContentType': response.get('ContentType'),
            'LastModified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
            'ETag': response.get('ETag'),
            'Metadata': response.get('Metadata', {}), # Custom user-defined metadata
            'ServerSideEncryption': response.get('ServerSideEncryption'),
            'VersionId': response.get('VersionId'),
        }
        return {k: v for k, v in metadata.items() if v is not None}
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            print(f"Object {object_key} not found in bucket {bucket_name}.")
            return {}
        else:
            print(f"Error retrieving object metadata: {e}")
            raise

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with actual bucket name and object key for testing.
    # Ensure you have AWS credentials configured.
    # metadata = get_object_metadata("your-s3-bucket-name", "example-upload.txt")
    # print(f"Object Metadata: {metadata}")
    pass
