import os
import boto3

def list_objects_with_prefix(bucket_name: str, prefix: str):
    """
    Lists objects in an S3 bucket that start with a given prefix.
    """
    s3_client = boto3.client('s3')
    objects = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append({
                        "Key": obj["Key"],
                        "Size": obj["Size"],
                        "LastModified": obj["LastModified"]
                    })
        return objects
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # Replace with actual values for testing
    # BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    # PREFIX = "my-folder/"
    # listed_objects = list_objects_with_prefix(BUCKET, PREFIX)
    # if listed_objects:
    #     print(f"Objects in {BUCKET} with prefix '{PREFIX}':")
    #     for obj in listed_objects:
    #         print(f"  Key: {obj['Key']}, Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']}")
    # else:
    #     print(f"No objects found with prefix '{PREFIX}'.")
    pass
