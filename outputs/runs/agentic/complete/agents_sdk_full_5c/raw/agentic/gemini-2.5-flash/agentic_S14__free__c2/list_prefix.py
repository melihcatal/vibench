import boto3
from storage_client import get_s3_client
from typing import List, Dict, Any

def list_objects_with_prefix(bucket_name: str, prefix: str = '') -> List[Dict[str, Any]]:
    """
    Lists stored objects under a bucket or container prefix in AWS S3.
    """
    s3_client = get_s3_client()
    
    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')
    
    try:
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in pages:
            for obj in page.get('Contents', []):
                objects.append({
                    'Key': obj.get('Key'),
                    'LastModified': obj.get('LastModified').isoformat() if obj.get('LastModified') else None,
                    'ETag': obj.get('ETag'),
                    'Size': obj.get('Size'),
                    'StorageClass': obj.get('StorageClass'),
                })
        return objects
    except s3_client.exceptions.ClientError as e:
        print(f"Error listing objects with prefix: {e}")
        raise

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with actual bucket name and prefix for testing.
    # Ensure you have AWS credentials configured.
    # objects_list = list_objects_with_prefix("your-s3-bucket-name", "your-prefix/")
    # for obj in objects_list:
    #     print(obj)
    pass
