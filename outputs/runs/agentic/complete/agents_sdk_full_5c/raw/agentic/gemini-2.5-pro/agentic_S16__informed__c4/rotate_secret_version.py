import os
import requests
from typing import Optional
from security_models import Secret

def get_staged_secret_from_doppler(project: str, config: str, secret_name: str) -> Optional[Secret]:
    """
    Reads a specific secret from a Doppler config (environment).

    Args:
        project: The name of the project in Doppler.
        config: The name of the config (e.g., 'dev', 'stg', 'prd').
        secret_name: The name of the secret.

    Returns:
        A Secret object or None if not found.
    """
    doppler_token = os.environ.get("DOPPLER_TOKEN")
    if not doppler_token:
        return None

    url = "https://api.doppler.com/v3/configs/config/secrets"
    headers = {"Authorization": f"Bearer {doppler_token}"}
    params = {"project": project, "config": config}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        secret_value = data.get("secrets", {}).get(secret_name, {}).get("raw")

        if secret_value:
            return Secret(name=secret_name, value=secret_value)
        return None
    except requests.exceptions.RequestException:
        return None
