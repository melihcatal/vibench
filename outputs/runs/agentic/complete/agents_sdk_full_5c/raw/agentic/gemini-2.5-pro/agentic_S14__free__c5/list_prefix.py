import os
from typing import List
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import StoredObject

def list_objects_by_prefix(bucket_name: str, prefix: str) -> List[StoredObject]:
    """
    Lists objects in an S3 bucket that match a given prefix.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: The prefix to filter objects by.

    Returns:
        A list of StoredObject models representing the found objects.
    """
    s3_client = get_storage_client()
    found_objects = []
    paginator = s3_client.get_paginator('list_objects_v2')

    try:
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in pages:
            if "Contents" in page:
                for obj_data in page["Contents"]:
                    # ETag often includes quotes which should be removed
                    obj_data['ETag'] = obj_data.get('ETag', '').strip('"')
                    stored_object = StoredObject(**obj_data)
                    found_objects.append(stored_object)
        return found_objects
    except ClientError as e:
        print(f"Error listing objects in bucket '{bucket_name}' with prefix '{prefix}': {e}")
        return []

# Example usage
# if __name__ == '__main__':
#     BUCKET = os.environ.get("AWS_S3_BUCKET")
#     PREFIX = "test-" # Assuming objects with this prefix exist
#     if BUCKET:
#         objects = list_objects_by_prefix(BUCKET, PREFIX)
#         if objects:
#             print(f"Found {len(objects)} objects with prefix '{PREFIX}':")
#             for obj in objects:
#                 print(f" - {obj.key} (Size: {obj.size} bytes)")
#         else:

#             print(f"No objects found with prefix '{PREFIX}'.")
#     else:
#         print("AWS_S3_BUCKET environment variable not set.")
