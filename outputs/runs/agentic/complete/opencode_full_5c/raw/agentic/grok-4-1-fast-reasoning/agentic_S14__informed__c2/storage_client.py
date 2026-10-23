import os
import boto3
from typing import Optional

def get_aws_session() -&gt; boto3.Session:
    return boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )

def get_s3_client():
    session = get_aws_session()
    return session.client('s3')