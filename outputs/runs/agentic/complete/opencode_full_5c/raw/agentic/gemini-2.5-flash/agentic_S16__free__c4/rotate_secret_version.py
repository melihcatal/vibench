from typing import Union, Dict, Any
from security_client import SecretsManagerClient


# AWS Secrets Manager is used to read a specific secret version or staged value.
def read_secret_version(
    secret_name: str, version_id: str = None, version_stage: str = None
) -> Union[str, Dict[str, Any]]:
    client = SecretsManagerClient()
    secret_value = client.get_secret(
        secret_name, version_id=version_id, version_stage=version_stage
    )
    return secret_value
