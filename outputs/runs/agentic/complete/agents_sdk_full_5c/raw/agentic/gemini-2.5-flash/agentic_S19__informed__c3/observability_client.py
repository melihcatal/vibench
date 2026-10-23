import os
import boto3

class CloudWatchClient:
    """
    Provides a configured boto3 client for Amazon CloudWatch.
    """
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get('AWS_REGION', 'us-east-1')
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = boto3.client(
                'cloudwatch',
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
        return self._client

