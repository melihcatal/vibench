import os
import json
import requests


def get_doppler_secret(
    token: str = os.getenv("DOPPLER_TOKEN"), secret_key: str = "API_KEY"
) -> dict:
    """Retrieve a secret from Doppler via its REST API.

    Returns the secret payload as a dict.
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://api.doppler.com/v3/secrets/get/{secret_key}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
