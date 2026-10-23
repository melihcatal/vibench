import boto3
import os

class CloudWatchClient:
    """
    Provides a configured AWS CloudWatch client.
    """
    def __init__(self, region_name: str = None):
        self.region_name = region_name if region_name else os.environ.get('AWS_REGION', 'us-east-1')
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = boto3.client(
                'cloudwatch',
                region_name=self.region_name,
                aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
            )
        return self._client

