
import os
from urllib.parse import urlencode

class IdentityClient:
    def __init__(self):
        self.client_id = os.environ.get("AZURE_AD_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_AD_CLIENT_SECRET")
        self.authority = os.environ.get("AZURE_AD_AUTHORITY", "https://login.microsoftonline.com/common")
        self.redirect_uri = os.environ.get("AZURE_AD_REDIRECT_URI", "http://localhost:5000/callback")
        self.scope = os.environ.get("AZURE_AD_SCOPE", "openid profile email offline_access User.Read")

    def get_authorization_url(self, state: str, code_challenge: str = None) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": state,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        
        # Microsoft identity platform authorization endpoint
        return f"{self.authority}/oauth2/v2.0/authorize?{urlencode(params)}"

    def get_token_url(self) -> str:
        return f"{self.authority}/oauth2/v2.0/token"

