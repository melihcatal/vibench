import os
import json

# Alibaba KMS Secrets Manager integration
from alibabacloud_kms20201212.client import Client as KmsClient
from alibabacloud_tea_openapi.models import Config

# Configuration (normally loaded from env or config file)
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION = os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou")
SECRET_NAME = "my-rotating-secret"


def rotate_secret_version() -> dict:
    """Reads a specific secret version or staged value from Alibaba KMS Secrets Manager.
    Returns:
        The secret payload as a dict.
    Raises:
        RuntimeError: If the read operation fails.
    """
    config = Config(
        access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        region_id=REGION,
    )
    kms = KmsClient(config)
    request = {
        "KeyAlias": SECRET_NAME,
        # Use either VersionId or Staging flag; here we demonstrate reading the latest version
        "VersionId": "1",
    }
    response = kms.get_secret_value(request)
    # The response format follows Alibaba Cloud SDK conventions
    return json.loads(response.to_json_string())
