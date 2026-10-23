import os
from urllib.parse import urlencode

import requests

from identity_models import normalize_scopes


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault("domain_prefix", os.getenv("COGNITO_DOMAIN_PREFIX", "example"))
    config.setdefault("region", os.getenv("AWS_REGION", "us-east-1"))
    config.setdefault("client_id", os.getenv("COGNITO_CLIENT_ID", ""))
    config.setdefault("client_secret", os.getenv("COGNITO_CLIENT_SECRET", ""))
    config.setdefault("identity_provider", os.getenv("COGNITO_IDENTITY_PROVIDER"))
    return config


def cognito_authorize_url(config, redirect_uri, state, scopes=None, code_challenge=None):
    base = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/authorize"
    query = {"response_type": "code", "client_id": config["client_id"], "redirect_uri": redirect_uri, "scope": " ".join(normalize_scopes(scopes) or ["openid", "email", "profile"]), "state": state}
    if config.get("identity_provider"):
        query["identity_provider"] = config["identity_provider"]
    if code_challenge:
        query["code_challenge"] = code_challenge
        query["code_challenge_method"] = "S256"
    return base + "?" + urlencode(query)


def exchange_code_for_tokens(config, code, redirect_uri, code_verifier=None):
    token_url = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/token"
    data = {"grant_type": "authorization_code", "client_id": config["client_id"], "code": code, "redirect_uri": redirect_uri}
    if code_verifier:
        data["code_verifier"] = code_verifier
    auth = None
    if config.get("client_secret"):
        auth = (config["client_id"], config["client_secret"])
        data.pop("client_id", None)
    response = requests.post(token_url, data=data, auth=auth, timeout=15)
    response.raise_for_status()
    return response.json()
