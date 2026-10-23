import os
import boto3
from botocore.config import Config

def get_translation_client():
    return boto3.client(
        service_name='translate',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        config=Config(
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            }
        )
    )