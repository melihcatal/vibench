import os
from typing import List
from security_client import AWSSecretsManagerClient
from security_models import RotationStatus

def rotation_summary() -> List[RotationStatus]:
    client = AWSSecretsManagerClient()
    secrets_list_response = client.list_secrets()
    summary_list = []

    for secret in secrets_list_response.get('SecretList', []):
        secret_name = secret.get('Name')
        rotation_enabled = secret.get('RotationEnabled', False)
        last_rotated_date = secret.get('LastRotatedDate')
        next_rotation_date = secret.get('NextRotationDate')

        summary_list.append(RotationStatus(
            secret_name=secret_name,
            rotation_enabled=rotation_enabled,
            last_rotated_date=last_rotated_date,
            next_rotation_date=next_rotation_date
        ))
    return summary_list
