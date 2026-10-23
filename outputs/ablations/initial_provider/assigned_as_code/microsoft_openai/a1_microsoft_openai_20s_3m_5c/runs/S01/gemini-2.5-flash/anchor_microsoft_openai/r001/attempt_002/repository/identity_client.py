import os
import msal
import requests

class IdentityClient:
    def __init__(self, client_id, client_secret, tenant_id, issuer=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.issuer = issuer
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )

    def _acquire_token_for_client(self, scopes=None):
        scopes = scopes or ['https://graph.microsoft.com/.default']
        token_result = self.app.acquire_token_for_client(scopes=scopes)
        if 'access_token' not in token_result:
            raise RuntimeError(f"Failed to acquire token: {token_result.get('error_description', token_result.get('error')}")
        return token_result['access_token']

    def get_ms_graph_client_headers(self):
        access_token = self._acquire_token_for_client()
        return {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

    # Potentially add methods for user-specific token flows if needed later
    # For email/password login, we will likely interact directly with Azure AD endpoints
    # rather than MS Graph for authentication itself, and then use MS Graph for user management.


def get_identity_client_from_env():
    client_id = os.environ.get("AZURE_AD_CLIENT_ID")
    client_secret = os.environ.get("AZURE_AD_CLIENT_SECRET")
    tenant_id = os.environ.get("AZURE_AD_TENANT_ID")
    issuer = os.environ.get("AZURE_AD_ISSUER") # Optional, can be derived or not needed depending on flow

    if not all([client_id, client_secret, tenant_id]):
        raise ValueError("Missing one or more Azure AD environment variables: AZURE_AD_CLIENT_ID, AZURE_AD_CLIENT_SECRET, AZURE_AD_TENANT_ID")

    return IdentityClient(client_id, client_secret, tenant_id, issuer)
