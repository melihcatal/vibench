import msal
import os

class IdentityClient:
    def __init__(self, client_id, tenant_id, client_secret, scope=None):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.scope = scope or ["https://graph.microsoft.com/.default"]
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority, client_credential=self.client_secret
        )

    def acquire_token_for_client(self):
        result = self.app.acquire_token_for_client(scopes=self.scope)
        if "access_token" not in result:
            raise RuntimeError("Failed to acquire token from Microsoft Identity Platform")
        return result["access_token"]

    def acquire_token_on_behalf_of(self, user_assertion, scopes=None):
        scopes = scopes or ["User.Read"]
        result = self.app.acquire_token_on_behalf_of(
            user_assertion=user_assertion, scopes=scopes
        )
        if "access_token" not in result:
            raise RuntimeError("Failed to acquire token on behalf of user")
        return result["access_token"]
