import os
from urllib.parse import urlencode


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.callback_url = os.environ.get("AUTH0_CALLBACK_URL")
        if not all([self.domain, self.client_id, self.callback_url]):
            raise ValueError(
                "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CALLBACK_URL must be set as environment variables."
            )

    def get_authorize_url(
        self, state: str, code_challenge: Optional[str] = None
    ) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "scope": "openid profile email",
            "state": state,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"

        return f"https://{self.domain}/authorize?{urlencode(params)}"

    def get_token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    def get_userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"
