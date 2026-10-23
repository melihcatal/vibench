import os
import json
import requests
from msal import PublicClientApplication, ConfidentialClientApplication


class MicrosoftEntraIdentityClient:
    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["openid", "profile", "email"]
        self.public_client = PublicClientApplication(
            client_id=self.client_id, authority=self.authority
        )
        self.confidential_client = None

    def get_auth_url(
        self,
        redirect_uri: str,
        state: str,
        code_challenge: str = None,
        code_challenge_method: str = None,
    ) -> str:
        auth_url = self.public_client.get_authorization_request_url(
            scopes=self.scope,
            redirect_uri=redirect_uri,
            state=state,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )
        return auth_url

    def exchange_code_for_token(
        self, redirect_uri: str, code: str, code_verifier: str = None
    ) -> dict:
        result = self.public_client.acquire_token_by_authorization_code(
            code=code,
            scopes=self.scope,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )
        return result

    def get_user_info(self, token: str) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://graph.microsoft.com/oidc/userinfo", headers=headers
        )
        response.raise_for_status()
        return response.json()
