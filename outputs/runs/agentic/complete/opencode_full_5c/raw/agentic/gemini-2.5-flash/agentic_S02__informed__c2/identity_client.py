import os


class Auth0Config:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.callback_url = os.environ.get("AUTH0_CALLBACK_URL")
        self.audience = f"https://{self.domain}/api/v2/"

        if not all([self.domain, self.client_id, self.callback_url]):
            raise ValueError("Auth0 environment variables are not fully set.")

    def get_authorize_url(
        self,
        response_type: str,
        scope: str,
        code_challenge: str = None,
        code_challenge_method: str = None,
    ):
        params = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "scope": scope,
            "audience": self.audience,
        }
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method

        import urllib.parse

        return f"https://{self.domain}/authorize?{urllib.parse.urlencode(params)}"

    def get_token_url(self):
        return f"https://{self.domain}/oauth/token"

    def get_userinfo_url(self):
        return f"https://{self.domain}/userinfo"


auth0_config = Auth0Config()
