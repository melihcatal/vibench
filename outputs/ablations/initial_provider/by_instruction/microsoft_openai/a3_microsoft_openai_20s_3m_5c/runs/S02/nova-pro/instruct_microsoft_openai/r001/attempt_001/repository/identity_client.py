import os

def get_config():
    return {
        'client_id': os.getenv('CLIENT_ID'),
        'tenant_id': os.getenv('TENANT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI')
    }

def create_client():
    config = get_config()
    return msal.PublicClientApplication(
        client_id=config['client_id'],
        authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret']
    )