import boto3
import os

class SecurityClient:
    def __init__(self):
        self.kms_client = boto3.client(
            'kms',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.comprehend_client = boto3.client(
            'comprehend',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.translate_client = boto3.client(
            'translate',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

    def get_kms_client(self):
        return self.kms_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_translate_client(self):
        return self.translate_client
