import os
import boto3
from botocore.exceptions import NoCredentialsError

class StorageClient:
    _s3_client = None

    @classmethod
    def get_client(cls):
        if cls._s3_client is None:
            try:
                cls._s3_client = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')
                )
            except NoCredentialsError:
                raise ValueError("AWS credentials not found. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables.")
        return cls._s3_client
