import os
from storage_client import get_s3_client
from storage_models import StorageObject

def upload_object(storage_object: StorageObject):
    s3_client = get_s3_client()
    try:
        s3_client.put_object(
            Bucket=storage_object.bucket_name,
            Key=storage_object.key,
            Body=storage_object.content,
            ContentType=storage_object.content_type
        )
        print(f"Object '''{storage_object.key}''' uploaded to bucket '''{storage_object.bucket_name}''' successfully.")
        return True
    except Exception as e:
        print(f"Error uploading object: {e}")
        return False
