import msal
import os


def get_identity_client():
    config = {
        'client_id': os.getenv('AZURE_CLIENT_ID'),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'tenant_id': os.getenv('AZURE_TENANT_ID'),
    }
    return msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])