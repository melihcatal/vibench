import os

class IdentityConfig:
    def __init__(self):
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        self.tenant_id = os.environ.get("AZURE_TENANT_ID", "common")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = os.environ.get("AZURE_SCOPE", "User.Read openid profile offline_access").split()

