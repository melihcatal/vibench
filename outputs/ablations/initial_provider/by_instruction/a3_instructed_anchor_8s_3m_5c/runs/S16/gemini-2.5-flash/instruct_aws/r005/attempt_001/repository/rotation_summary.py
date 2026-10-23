from security_client import SecretsManagerClient
from typing import Dict, Any, List, Optional

def summarize_secret_rotation_status(secret_id: str, region_name: str = 'us-east-1') -> Optional[Dict[str, Any]]:
    client = SecretsManagerClient(region_name=region_name)
    secret_info = client.describe_secret(secret_id)
    
    if not secret_info:
        return None

    summary = {
        'SecretId': secret_info.get('Name'),
        'ARN': secret_info.get('ARN'),
        'LastRotatedDate': secret_info.get('LastRotatedDate'),
        'RotationEnabled': secret_info.get('RotationEnabled'),
        'RotationLambdaARN': secret_info.get('RotationLambdaARN'),
        'NextRotationDate': secret_info.get('NextRotationDate'),
        'VersionStages': secret_info.get('VersionIdsToStages', {})
    }
    
    return summary
