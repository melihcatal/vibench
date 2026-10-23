import boto3
import os
from datetime import datetime, timedelta
from typing import Tuple

region = os.getenv('AWS_REGION', 'us-east-1')
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=region
)
cloudwatch_client = session.client('cloudwatch')
s3_client = session.client('s3')

def get_time_window(hours: float = 1.0) -> Tuple[datetime, datetime]:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    return start_time, end_time