import os
import boto3

class SpeechClient:
    def __init__(self):
        self.transcribe_client = boto3.client(
            'transcribe',
            region_name=os.environ.get('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def get_client(self):
        return self.transcribe_client
