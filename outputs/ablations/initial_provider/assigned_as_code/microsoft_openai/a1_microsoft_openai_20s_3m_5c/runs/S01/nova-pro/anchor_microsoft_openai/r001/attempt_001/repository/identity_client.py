import os
import msal


def get_client(config=None):
    config = config or {}
    client_id = config.get('client_id', os.getenv('CLIENT_ID'))
    tenant_id = config.get('tenant_id', os.getenv('TENANT_ID'))
    client_secret = config.get('client_secret', os.getenv('CLIENT_SECRET'))
    return msal.ConfidentialClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret)