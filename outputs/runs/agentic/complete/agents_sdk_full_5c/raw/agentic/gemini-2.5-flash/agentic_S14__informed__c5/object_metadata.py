import os
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata | None:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        metadata = response['ResponseMetadata']['HTTPHeaders']
        print(f"Metadata for '''{object_key}''' retrieved successfully.")
        return ObjectMetadata(
            bucket_name=bucket_name,
            key=object_key,
            etag=response.get('ETag', '').strip('\'\'\'), # Remove quotes from ETag
            size=response.get('ContentLength', 0),
            last_modified=response.get('LastModified', '').isoformat(),
            content_type=response.get('ContentType', '')
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Object '''{object_key}''' not found in bucket '''{bucket_name}'''.")
        else:
            print(f"Error retrieving object metadata: {e}")
        return None
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        return None
