import os
from typing import Dict

def get_aws_credentials() -> Dict[str, str]:
    region = os.getenv('AWS_REGION', 'us-east-1')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not access_key or not secret_key:
        raise ValueError(
            "AWS credentials must be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )
    
    return {
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key,
        'region_name': region
    }

def get_aws_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')
