# HELPER: identity_client.py
# Local configuration and client utilities for Federated Login Flow

import os
import json
from typing import Any, Dict

# Provider configuration (example using Auth0; can be swapped)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/oauth_callback"


# Simple configuration loader (supports environment or JSON file)
def load_config(config_path: str = None) -> Dict[str, Any]:
    if config_path:
        with open(config_path, "r") as f:
            return json.load(f)
    # Default to env vars
    return {
        "domain": AUTH0_DOMAIN,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }


# Basic client helper to call Auth0 userinfo endpoint
def call_userinfo(access_token: str) -> Dict[str, Any]:
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    import requests

    resp = requests.get(userinfo_url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# Example usage (for testing)
if __name__ == "__main__":
    cfg = load_config()
    print("Loaded config:", cfg)
