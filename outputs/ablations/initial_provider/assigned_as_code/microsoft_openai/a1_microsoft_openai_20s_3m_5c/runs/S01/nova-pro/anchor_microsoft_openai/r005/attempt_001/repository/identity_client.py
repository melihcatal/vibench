import os

def get_identity_client():
    return {
        'client_id': os.getenv('AZURE_CLIENT_ID'),
        'tenant_id': os.getenv('AZURE_TENANT_ID'),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'issuer': os.getenv('AZURE_ISSUER')
    }