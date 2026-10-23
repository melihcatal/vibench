import boto3
import os

class MessagingClient:
    def __init__(self, region_name=None):
        if region_name is None:
            region_name = os.environ.get('AWS_REGION', 'us-east-1')

        self.sns_client = boto3.client('sns', region_name=region_name)
        self.sqs_client = boto3.client('sqs', region_name=region_name)

    def get_sns_client(self):
        return self.sns_client

    def get_sqs_client(self):
        return self.sqs_client
