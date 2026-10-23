import os
import msal

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")


def get_client():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    return msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)


if __name__ == "__main__":
    client = get_client()
