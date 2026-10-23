import os
import json
import urllib.request
from dataclasses import dataclass

@dataclass
class IdentitySettings:
    base_url: str
    api_key: str
    timeout: float

@dataclass
class IdentityClient:
    headers: dict
    settings: IdentitySettings

def load_settings():
    return IdentitySettings(base_url=os.environ.get('IDENTITY_API_BASE_URL', 'https://api.example.com'), api_key=os.environ.get('IDENTITY_API_KEY', ''), timeout=float(os.environ.get('IDENTITY_TIMEOUT', '30')))

def build_identity_client():
    settings = load_settings()
    return IdentityClient(headers={'Authorization': f'Bearer {settings.api_key}', 'Content-Type': 'application/json'}, settings=settings)

def build_json_request(url, payload, method='POST', headers=None):
    body = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(url, data=body, method=method)
    for k, v in (headers or {}).items():
        request.add_header(k, v)
    return request
