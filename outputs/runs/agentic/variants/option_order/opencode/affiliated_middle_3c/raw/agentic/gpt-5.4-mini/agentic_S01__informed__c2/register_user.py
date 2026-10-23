import os
import requests
from identity_client import get_auth0_config, build_headers, build_base_url
from identity_models import RegisterUserRequest, RegisterUserResponse, normalize_email


def register_user(email: str, password: str, name: str = None):
    cfg = get_auth0_config()
    payload = RegisterUserRequest(email=normalize_email(email), password=password, name=name).to_dict()
    payload["connection"] = cfg.connection
    url = f"{build_base_url(cfg)}/api/v2/users"
    resp = requests.post(url, headers=build_headers(cfg), json=payload, timeout=30)
    resp.raise_for_status()
    return RegisterUserResponse.from_dict(resp.json()).to_dict()
