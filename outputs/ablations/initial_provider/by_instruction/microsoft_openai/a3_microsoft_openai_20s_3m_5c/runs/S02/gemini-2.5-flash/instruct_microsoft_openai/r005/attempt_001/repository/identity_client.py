import os
from urllib.parse import urlencode

class IdentityClient:
    def __init__(self):
        self.tenant_id = os.environ.get("AZURE_AD_TENANT_ID", "YOUR_AZURE_AD_TENANT_ID")
        self.client_id = os.environ.get("AZURE_AD_CLIENT_ID", "YOUR_AZURE_AD_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_AD_CLIENT_SECRET", "YOUR_AZURE_AD_CLIENT_SECRET")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.authorization_endpoint = f"{self.authority}/oauth2/v2.0/authorize"
        self.token_endpoint = f"{self.authority}/oauth2/v2.0/token"
        self.userinfo_endpoint = "https://graph.microsoft.com/oidc/userinfo"
        self.scope = "openid profile email offline_access User.Read"

    def get_authorization_url(self, redirect_uri: str, state: str, code_challenge: str = None) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "response_mode": "query",
            "scope": self.scope,
            "state": state,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        return f"{self.authorization_endpoint}?{urlencode(params)}"
