import os
from storage_client import get_s3_client
from storage_models import PresignedUrl

def create_presigned_download_url(bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> PresignedUrl | None:
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_seconds
        )
        print(f"Presigned URL for '''{object_key}''' created successfully.")
        return PresignedUrl(url=response, expires_in_seconds=expiration_seconds)
    except Exception as e:
        print(f"Error creating presigned URL: {e}")
        return None
