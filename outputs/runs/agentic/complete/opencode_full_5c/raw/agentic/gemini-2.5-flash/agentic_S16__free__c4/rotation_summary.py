from typing import List
from datetime import datetime
from security_client import SecretsManagerClient
from security_models import RotationStatus


# AWS Secrets Manager is used to summarize secret rotation status.
def summarize_rotation_status() -> List[RotationStatus]:
    client = SecretsManagerClient()
    secrets_list_response = client.list_secrets()
    summary_list = []

    for secret in secrets_list_response.get("SecretList", []):
        secret_name = secret["Name"]
        describe_secret_response = client.describe_secret(secret_name)

        rotation_enabled = describe_secret_response.get("RotationEnabled", False)
        last_rotated_date_timestamp = describe_secret_response.get("LastRotatedDate")
        last_rotated_date = None
        if last_rotated_date_timestamp:
            last_rotated_date = datetime.fromtimestamp(
                last_rotated_date_timestamp.timestamp()
            ).isoformat()

        summary_list.append(
            RotationStatus(
                secret_name=secret_name,
                rotation_enabled=rotation_enabled,
                last_rotated_date=last_rotated_date,
            )
        )
    return summary_list
