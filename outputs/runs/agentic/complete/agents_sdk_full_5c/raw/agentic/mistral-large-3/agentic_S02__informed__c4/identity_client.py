import os
import requests
from typing import Dict, Any


def get_oidc_config(well_known_url: str) -> Dict[str, Any]:
    response = requests.get(well_known_url)
    response.raise_for_status()
    return response.json()


def load_provider_config(provider: str):
    configs = {
        "auth0": {
            "domain": os.getenv("AUTH0_DOMAIN"),
            "client_id": os.getenv("AUTH0_CLIENT_ID"),
            "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
            "callback_url": os.getenv("AUTH0_CALLBACK_URL")
        }
    }
    return configs.get(provider)