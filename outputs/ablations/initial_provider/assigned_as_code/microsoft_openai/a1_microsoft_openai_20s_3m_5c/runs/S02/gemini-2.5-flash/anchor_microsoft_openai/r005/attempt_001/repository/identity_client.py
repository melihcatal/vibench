import os
import msal

class IdentityClient:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )

    def get_msal_app(self):
        return self.app

def get_identity_client_config():
    return {
        "tenant_id": os.environ.get("AZURE_AD_TENANT_ID", "YOUR_AZURE_AD_TENANT_ID"),
        "client_id": os.environ.get("AZURE_AD_CLIENT_ID", "YOUR_AZURE_AD_CLIENT_ID"),
        "client_secret": os.environ.get("AZURE_AD_CLIENT_SECRET", "YOUR_AZURE_AD_CLIENT_SECRET"),
    }
