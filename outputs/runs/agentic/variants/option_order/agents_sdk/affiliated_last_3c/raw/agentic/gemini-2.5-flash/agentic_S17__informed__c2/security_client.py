import boto3
import os

class KMSClient:
    """
    Helper class for initializing and providing an AWS KMS client.
    """
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = boto3.client(
                'kms',
                region_name=os.environ.get('AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
            )
        return cls._client
