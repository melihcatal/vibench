import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Dict, Any


def generate_pkce_parameters():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_bytes).decode().rstrip("=")

    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }


def start_pkce_login(provider: str = "okta") -> Dict[str, Any]:
    if provider == "okta":
        client_id = os.environ.get("OKTA_CLIENT_ID")
        okta_domain = os.environ.get("OKTA_DOMAIN")
        redirect_uri = os.environ.get(
            "OKTA_REDIRECT_URI", "http://localhost:8000/callback"
        )

        if not okta_domain:
            raise ValueError("OKTA_DOMAIN environment variable is required")

        pkce_params = generate_pkce_parameters()

        auth_endpoint = f"https://{okta_domain}/oauth2/default/v1/authorize"

        params = {
            "client_id": client_id,
            "response_type": "code",
            "scope": "openid profile email",
            "redirect_uri": redirect_uri,
            "state": secrets.token_urlsafe(16),
            "code_challenge": pkce_params["code_challenge"],
            "code_challenge_method": pkce_params["code_challenge_method"],
        }

        auth_url = f"{auth_endpoint}?{urllib.parse.urlencode(params)}"

        return {
            "auth_url": auth_url,
            "state": params["state"],
            "code_verifier": pkce_params["code_verifier"],
            "provider": "okta",
        }

    elif provider == "azure_ad":
        client_id = os.environ.get("AZURE_CLIENT_ID")
        tenant_id = os.environ.get("AZURE_TENANT_ID", "common")
        redirect_uri = os.environ.get(
            "AZURE_REDIRECT_URI", "http://localhost:8000/callback"
        )

        pkce_params = generate_pkce_parameters()

        auth_endpoint = (
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
        )

        params = {
            "client_id": client_id,
            "response_type": "code",
            "scope": "openid profile email",
            "redirect_uri": redirect_uri,
            "state": secrets.token_urlsafe(16),
            "code_challenge": pkce_params["code_challenge"],
            "code_challenge_method": pkce_params["code_challenge_method"],
            "response_mode": "query",
        }

        auth_url = f"{auth_endpoint}?{urllib.parse.urlencode(params)}"

        return {
            "auth_url": auth_url,
            "state": params["state"],
            "code_verifier": pkce_params["code_verifier"],
            "provider": "azure_ad",
        }

    elif provider == "cognito":
        client_id = os.environ.get("COGNITO_CLIENT_ID")
        cognito_domain = os.environ.get("COGNITO_DOMAIN")
        redirect_uri = os.environ.get(
            "COGNITO_REDIRECT_URI", "http://localhost:8000/callback"
        )

        if not cognito_domain:
            raise ValueError("COGNITO_DOMAIN environment variable is required")

        pkce_params = generate_pkce_parameters()

        auth_endpoint = f"https://{cognito_domain}/oauth2/authorize"

        params = {
            "client_id": client_id,
            "response_type": "code",
            "scope": "openid profile email",
            "redirect_uri": redirect_uri,
            "state": secrets.token_urlsafe(16),
            "code_challenge": pkce_params["code_challenge"],
            "code_challenge_method": pkce_params["code_challenge_method"],
        }

        auth_url = f"{auth_endpoint}?{urllib.parse.urlencode(params)}"

        return {
            "auth_url": auth_url,
            "state": params["state"],
            "code_verifier": pkce_params["code_verifier"],
            "provider": "cognito",
        }

    else:
        raise ValueError(f"Unsupported provider for PKCE: {provider}")
