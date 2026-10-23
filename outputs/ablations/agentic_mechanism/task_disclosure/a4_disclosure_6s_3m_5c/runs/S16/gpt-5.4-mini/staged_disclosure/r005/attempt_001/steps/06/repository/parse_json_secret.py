import json
import os
from typing import Any, Dict

import requests


TWILIO_API_BASE = "https://secrets.twilio.com"


def retrieve_and_parse_json_secret(secret_name: str) -> Dict[str, Any]:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    url = f"{TWILIO_API_BASE}/v1/Secrets/{secret_name}"
    response = requests.get(url, auth=(account_sid, auth_token), timeout=30)
    response.raise_for_status()
    payload = response.json()
    secret_value = payload.get("secret_value") or payload.get("value")
    if secret_value is None:
        raise ValueError("Secret payload did not include a JSON secret value")
    if isinstance(secret_value, dict):
        return secret_value
    if isinstance(secret_value, str):
        return json.loads(secret_value)
    raise TypeError("Unsupported secret value type")
