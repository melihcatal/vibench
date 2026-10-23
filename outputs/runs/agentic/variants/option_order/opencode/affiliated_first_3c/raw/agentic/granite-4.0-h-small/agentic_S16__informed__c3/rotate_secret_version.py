# rotate_secret_version.py
# [SAME-SCENARIO]
# Reads a specific secret version or staged value from Alibaba KMS Secrets Manager

import os
from alibabacloud_secretsmanager20190930.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions


def rotate_secret_version(secret_name: str, version_id: str) -> str:
    """Retrieve a specific version (or staged value) of a secret from Alibaba Cloud Secrets Manager.

    Args:
        secret_name: Name/ARN of the secret.
        version_id: Version ID or 'staged' to get pending rotation.

    Returns:
        Plaintext value of the requested version.
    """
    access_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    secret_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key or not secret_key:
        raise RuntimeError(
            "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
        )

    config = Config(
        access_key_id=access_key,
        access_key_secret=secret_key,
        region_id="cn-hangzhou",  # adjust as needed
    )

    client = Client(config)
    request = client.get_secret_version(SecretName=secret_name, VersionId=version_id)
    result = request.body.decode("utf-8")
    return result
