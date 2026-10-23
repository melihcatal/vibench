import os
from typing import Dict, Optional
import requests

class IdentityClient:
    def __init__(self):
        self.ibm_appid_tenant_id = os.getenv("IBM_APPID_TENANT_ID")
        self.ibm_appid_client_id = os.getenv("IBM_APPID_CLIENT_ID")
        self.ibm_appid_secret = os.getenv("IBM_APPID_CLIENT_SECRET")
        self.ibm_appid_oauth_server_url = os.getenv("IBM_APPID_OAUTH_SERVER_URL")
        self.auth0_domain = os.getenv("AUTH0_DOMAIN")
        self.auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
        self.auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")

    def get_ibm_appid_tokens(self, code: str, redirect_uri: str) -> Optional[Dict]:
        token_url = f"{self.ibm_appid_oauth_server_url}/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.ibm_appid_client_id,
            "client_secret": self.ibm_appid_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        return response.json()