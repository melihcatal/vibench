# image_asset_archive.py
import json
import uuid
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import Dict, List

def archive_assets(analysis: Dict, bucket_name: str, prefix: str = "image_analysis") -> bool:
    """Upload analysis JSON to managed object storage (Amazon S3) and return success flag."""
    s3 = boto3.client('s3')
    key = f"{prefix}/{uuid.uuid4()}.json"
    try:
        s3.put_object(Body=json.dumps(analysis), Bucket=bucket_name, Key=key)
        return True
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"AWS credentials error: {e}")
    except Exception as e:
        print(f"Unexpected error uploading to S3: {e}")
    return False
