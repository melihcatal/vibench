from typing import Any, Dict

import requests

from identity_client import get_config


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    config = get_config()
    response = requests.post(
        f"https://securetoken.googleapis.com/v1/token?key={config['google_api_key']}",
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
