import os
import boto3
from typing import List
from storage_client import get_s3_client
from storage_models import ObjectSummary

def list_objects_with_prefix(bucket_name: str, prefix: str = "") -> List[ObjectSummary]:
    """
    Lists objects in an S3 bucket under a given prefix.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter objects by (default: empty string, lists all objects).

    Returns:
        List[ObjectSummary]: A list of ObjectSummary objects.
    """
    s3_client = get_s3_client()
    object_summaries: List[ObjectSummary] = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if "Contents" in page:
                for obj in page['Contents']:
                    object_summaries.append(ObjectSummary(
                        key=obj.get('Key'),
                        last_modified=obj.get('LastModified'),
                        size=obj.get('Size'),
                        e_tag=obj.get('ETag'),
                        storage_class=obj.get('StorageClass'),
                    ))
        print(f"Listed {len(object_summaries)} objects under prefix '{prefix}' in s3://{bucket_name}")
    except Exception as e:
        print(f"Error listing objects: {e}")
    return object_summaries

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and prefix)
    # Ensure AWS credentials are configured
    _bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-aws-s3-bucket-name")
    _prefix = "example-uploads/"

    objects = list_objects_with_prefix(_bucket_name, _prefix)
    if objects:
        print("\nObjects found:")
        for obj in objects:
            print(f"  - Key: {obj.key}, Size: {obj.size}, Last Modified: {obj.last_modified}")
    else:
        print("No objects found or an error occurred.")

    print("\nListing all objects (no prefix):")
    all_objects = list_objects_with_prefix(_bucket_name)
    if all_objects:
        print(f"Found {len(all_objects)} total objects.")
    else:
        print("No objects found or an error occurred.")
