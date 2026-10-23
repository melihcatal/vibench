import requests
import os
import json
from security_models import SecretRequest, SecretResponse

def fetch_api_key(req: SecretRequest) -> SecretResponse:
    token = os.getenv("DOPPLER_TOKEN")
    url = "https://api.doppler.com/v3/config/secrets/get"
    headers = {
        "Authorization": f"Dp api {token}",
        "Content-Type": "application/json"
    }
    body = {
        "config": req.config,
        "names": [req.name]
    }
    resp = requests.post(url, headers=headers, json=body)
    data = resp.json()
    value = data["item"]["secrets"][0]["value"]
    return SecretResponse(value=value, version=data["item"]["secrets"][0].get("version", "latest"))