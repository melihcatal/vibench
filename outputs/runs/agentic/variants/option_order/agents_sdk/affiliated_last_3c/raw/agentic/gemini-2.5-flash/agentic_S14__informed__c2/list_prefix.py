import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import StoredObject
from typing import List

def list_objects_with_prefix(bucket_name: str, prefix: str = '') -> List[StoredObject]:
    """
    Lists objects in an S3 bucket with a given prefix.
    """
    s3_client = get_s3_client()
    objects = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if "Contents" in page:
                for obj in page['Contents']:
                    objects.append(
                        StoredObject(
                            bucket_name=bucket_name,
                            object_name=obj['Key'],
                            last_modified=obj['LastModified'].isoformat(),
                            etag=obj['ETag'].strip('\"'),
                            size=obj['Size']
                        )
                    )
    except ClientError as e:
        print(f"Error listing objects: {e}")
    return objects

if __name__ == '__main__':
    # Example usage (replace with actual values)
    bucket = os.environ.get("S3_BUCKET_NAME", "my-test-bucket")
    prefix_to_list = "test/"
    listed_objects = list_objects_with_prefix(bucket, prefix_to_list)
    if listed_objects:
        print(f"Objects under prefix '{prefix_to_list}':")
        for obj in listed_objects:
            print(f" - {obj.object_name} (Size: {obj.size} bytes)")
    else:
        print(f"No objects found under prefix '{prefix_to_list}' or an error occurred.")
