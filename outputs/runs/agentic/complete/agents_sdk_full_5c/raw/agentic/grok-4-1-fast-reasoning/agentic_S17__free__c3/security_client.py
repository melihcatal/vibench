import boto3
import os
from typing import Any

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
kms_client = boto3.client('kms', region_name=AWS_REGION)
SYMMETRIC_KEY_ID = os.getenv('KMS_SYMMETRIC_KEY_ID')
ASYMMETRIC_KEY_ID = os.getenv('KMS_ASYMMETRIC_KEY_ID')
