import os
import msal
from identity_models import TokenResponse

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"


def get_confidential_app():
    return msal.ConfidentialClientApplication(
        AZURE_CLIENT_ID, authority=AUTHORITY, client_credential=AZURE_CLIENT_SECRET
    )


def get_public_app():
    return msal.PublicClientApplication(AZURE_CLIENT_ID, authority=AUTHORITY)


USERINFO_ENDPOINT = (
    f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/openid/v2.0/userinfo"
)
