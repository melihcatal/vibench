import requests
from typing import Dict, Any
from security_client import get_provider_config
from security_models import PlainSecret, SecretMetadata


def rotate_secret_version(
    config_name: str, secret_name: str, config_version: int
) -> PlainSecret:
    config = get_provider_config("doppler")
    token = config["token"]
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.doppler.com/v3/configs/{config_name}/secrets"
    params = {"include_resolved": "true", "config_version": config_version}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    secret_value = data["secret"][secret_name]
    metadata: SecretMetadata = {
        "name": secret_name,
        "version_id": str(config_version),
        "created_time": data.get("config", {}).get("updatedAt", ""),
    }
    return {"metadata": metadata, "value": secret_value}
