import boto3

class CloudWatchClient:
    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('cloudwatch', region_name=region_name)

    def get_cloudwatch_client(self):
        return self.client