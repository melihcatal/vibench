import webbrowser
import requests
from identity_client import Auth0Client
from identity_models import TokenResponse

class PKCELoginFlow:
    def __init__(self):
        self.client = Auth0Client()
        self.code_verifier, self.code_challenge = self.client.generate_pkce_pair()

    def get_authorize_url(self) -> str:
        return self.client.get_authorize_url(code_challenge=self.code_challenge)

    def start_login(self):
        url = self.get_authorize_url()
        print(f"Opening Auth0 PKCE login: {url}")
        print(f"Remember this code verifier: {self.code_verifier}")
        webbrowser.open(url)

    def exchange_code_for_tokens(self, code: str) -> TokenResponse:
        token_url = f"https://{self.client.domain}/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client.client_id,
            'code': code,
            'redirect_uri': self.client.redirect_uri,
            'code_verifier': self.code_verifier,
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        return TokenResponse(**resp.json())