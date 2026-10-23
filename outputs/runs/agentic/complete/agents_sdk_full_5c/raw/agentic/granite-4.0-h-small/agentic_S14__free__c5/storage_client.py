# storage_client.py
import os
from typing import Any, Dict
# Concreate provider SDK import example (AWS S3)
from boto3 import client as boto3_client

# Example of loading credentials/environment variables for AWS S3
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialise the concrete provider client once
s3 = boto3_client(
    service_name='s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

class ManagedStorageClient:
    """Local helper class that wraps the concrete provider client with common operations.

    All provider‑identifying signals appear here: import of boto3, use of AWS service name, and
    environment variables for credentials.
    """

    def upload(self, bucket: str, key: str, body: bytes, content_type: str) -> Dict[str, Any]:
        return s3.upload_fileobj(
            Fileobj=body,
            Bucket=bucket,
            Key=key,
            ExtraArgs={'ContentType': content_type}
        )

    def generate_presigned_url(self, bucket: str, key: str, expires_in: int) -> str:
        return s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )

    def head_object(self, bucket: str, key: str) -> Dict[str, Any]:
        return s3.head_object(Bucket=bucket, Key=key)

    def list_objects(self, bucket: str, prefix: str = '', delimiter: str = '') -> list[str]:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter=delimiter)
        # Return just the object keys (simplified)
        return [obj['Key'] for obj in resp.get('Contents', [])]

    def download(self, bucket: str, key: str) -> bytes:
        """Utility to fetch object bytes for downstream processing."""
        obj = s3.get_object(Bucket=bucket, Key=key)
        return obj['Body'].read()

    def download_text(self, bucket: str, key: str) -> str:
        return self.download(bucket, key).decode('utf-8')
