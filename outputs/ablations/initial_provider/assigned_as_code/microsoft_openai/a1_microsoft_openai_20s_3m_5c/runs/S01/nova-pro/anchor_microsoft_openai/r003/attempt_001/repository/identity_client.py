import os
import msal

def get_config():
    return {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'tenant_id': os.getenv('TENANT_ID'),
        'issuer': os.getenv('ISSUER'),
        'access_token': os.getenv('ACCESS_TOKEN')
    }

def get_client():
    config = get_config()
    return msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
