import boto3
import os

class ObservabilityClient:
    def __init__(self):
        self.client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.log_group_name = os.getenv('AWS_LOG_GROUP_NAME', 'my-application-logs')

    def get_client(self):
        return self.client

    def get_log_group_name(self):
        return self.log_group_name
