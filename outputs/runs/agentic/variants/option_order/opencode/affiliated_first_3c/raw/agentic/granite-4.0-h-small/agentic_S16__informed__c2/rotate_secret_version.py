import os
import json

# Provider-specific configuration
# Using Alibaba KMS Secrets Manager
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
ALIBABA_REGION = os.getenv("ALIBABA_REGION", "cn-hangzhou")
ALIBABA_SECRET_NAME = os.getenv("ALIBABA_SECRET_NAME")

from alibabacloud_kms20201214.client import Client as KmsClient
from alibabacloud_tea_util.model import Config

config = Config(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id=ALIBABA_REGION,
)
client = KmsClient(config)


def read_secret_version(secret_name: str, version_id: str) -> dict:
    """Read a specific secret version or staged value from Alibaba KMS Secrets Manager.
    Returns the secret payload as a dict.
    """
    request = {
        "secret_name": secret_name,
        "version_id": version_id,
    }
    response = client.get_secret_value(request)
    return json.loads(response.secret_data)


if __name__ == "__main__":
    secret_name = ALIBABA_SECRET_NAME
    version_id = os.getenv("SECRET_VERSION", "latest")
    if secret_name:
        print(
            "Secret version",
            version_id,
            ":",
            read_secret_version(secret_name, version_id),
        )
    else:
        print("Set ALIBABA_SECRET_NAME env var")
