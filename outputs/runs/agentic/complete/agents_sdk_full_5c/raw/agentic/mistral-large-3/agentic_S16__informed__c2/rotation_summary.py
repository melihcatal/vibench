import boto3
import os
from datetime import datetime

from security_models import RotationSummary

def rotation_summary(secret_name: str) -> RotationSummary:
    client = boto3.client(
        'secretsmanager',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    
    response = client.describe_secret(SecretId=secret_name)
    versions = response.get('VersionIdsToStages', {})
    
    current_version = next(
        (v for v, stages in versions.items() if 'AWSCURRENT' in stages), None
    )
    previous_version = next(
        (v for v, stages in versions.items() if 'AWSPREVIOUS' in stages), None
    )
    
    last_rotation = response.get('LastRotatedDate', datetime.now())
    rotation_status = "COMPLIANT" if (datetime.now() - last_rotation).days <= 90 else "NON_COMPLIANT"
    
    return RotationSummary(
        secret_name=secret_name,
        current_version=current_version,
        previous_version=previous_version,
        rotation_status=rotation_status
    )