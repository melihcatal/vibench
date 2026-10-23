import os
import msal


def get_confidential_client():
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    authority = f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}"

    return msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )


def get_public_client():
    client_id = os.environ["AZURE_CLIENT_ID"]
    authority = f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}"

    return msal.PublicClientApplication(client_id, authority=authority)


def get_default_scopes():
    return ["User.Read", "openid", "profile", "offline_access"]


def get_redirect_uri():
    return os.environ.get("AZURE_REDIRECT_URI", "http://localhost:8000/callback")
