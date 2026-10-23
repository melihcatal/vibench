import os
import msal

class IdentityClient:
    def __init__(self, client_id=None, tenant_id=None, client_secret=None, issuer=None):
        self.client_id = client_id or os.environ.get("AZURE_CLIENT_ID")
        self.tenant_id = tenant_id or os.environ.get("AZURE_TENANT_ID")
        self.client_secret = client_secret or os.environ.get("AZURE_CLIENT_SECRET")
        self.issuer = issuer or os.environ.get("AZURE_ISSUER")
        if not all([self.client_id, self.tenant_id, self.client_secret, self.issuer]):
            raise ValueError("Azure AD configuration missing. Ensure client_id, tenant_id, client_secret, and issuer are set.")
        
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.msal_app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority, client_credential=self.client_secret)

    def get_msal_app(self):
        return self.msal_app

    def get_config(self):
        return {
            "client_id": self.client_id,
            "tenant_id": self.tenant_id,
            "client_secret": self.client_secret,
            "issuer": self.issuer,
            "authority": self.authority
        }
