import os


def get_config():
    return {
        'client_id': os.getenv('AZURE_CLIENT_ID'),
        'tenant_id': os.getenv('AZURE_TENANT_ID'),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'issuer': 'https://sts.windows.net/' + os.getenv('AZURE_TENANT_ID') + '/'
    }
