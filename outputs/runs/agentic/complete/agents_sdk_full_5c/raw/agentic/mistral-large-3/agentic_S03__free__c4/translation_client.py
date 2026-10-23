import os
import boto3
from botocore.config import Config

def get_translation_client():
    """
    Initialize and return an AWS Translate client with configurable settings.
    """
    region = os.getenv('AWS_TRANSLATE_REGION', 'us-east-1')
    max_retries = int(os.getenv('AWS_TRANSLATE_MAX_RETRIES', '3'))
    
    config = Config(
        retries={
            'max_attempts': max_retries,
            'mode': 'adaptive'
        }
    )
    
    return boto3.client(
        service_name='translate',
        region_name=region,
        config=config
    )