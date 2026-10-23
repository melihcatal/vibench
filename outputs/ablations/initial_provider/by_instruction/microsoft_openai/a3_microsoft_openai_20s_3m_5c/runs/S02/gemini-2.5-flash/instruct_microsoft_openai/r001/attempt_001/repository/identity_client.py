import os
import urllib.parse

class MicrosoftIdentityClient:
    def __init__(self):
        self.client_id = os.environ.get("MICROSOFT_CLIENT_ID")
        self.client_secret = os.environ.get("MICROSOFT_CLIENT_SECRET")
        self.tenant_id = os.environ.get("MICROSOFT_TENANT_ID", "common")
        self.redirect_uri = os.environ.get("MICROSOFT_REDIRECT_URI")

        if not all([self.client_id, self.redirect_uri]):
            raise ValueError("MICROSOFT_CLIENT_ID and MICROSOFT_REDIRECT_URI must be set in environment variables.")

        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.authorize_endpoint = f"{self.authority}/oauth2/v2.0/authorize"
        self.token_endpoint = f"{self.authority}/oauth2/v2.0/token"
        self.graph_api_endpoint = "https://graph.microsoft.com/v1.0/me"

    def get_authorize_url(self, state: str, scope: str = "openid profile email", code_challenge: str = None) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
            "response_mode": "query"
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"

        query_string = urllib.parse.urlencode(params)
        return f"{self.authorize_endpoint}?{query_string}"

    def get_token_params(self, code: str, code_verifier: str = None, scope: str = "openid profile email offline_access") -> dict:
        params = {
            "client_id": self.client_id,
            "scope": scope,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        if self.client_secret:
            params["client_secret"] = self.client_secret
        if code_verifier:
            params["code_verifier"] = code_verifier
        return params

    def get_graph_api_headers(self, access_token: str) -> dict:
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

if __name__ == "__main__":
    # Example usage:
    # try:
    #     client = MicrosoftIdentityClient()
    #     print("Microsoft Identity Client initialized.")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
