import msal
import os

class IdentityClient:
    def __init__(self):
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.graph_api_base_url = "https://graph.microsoft.com/v1.0"
        
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError("Azure AD environment variables not set: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID")

        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )

    def get_access_token(self):
        result = self.app.acquire_token_for_client(scopes=self.scope)
        if "access_token" not in result:
            raise RuntimeError(f"Could not acquire access token: {result.get("error_description", "Unknown error")}")
        return result["access_token"]

