import os


def get_config():
    return {
        'client_id': os.getenv('CLIENT_ID'),
        'tenant_id': os.getenv('TENANT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
    }


def create_confidential_client(config):
    import msal
    return msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])


def create_public_client(config):
    import msal
    return msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")