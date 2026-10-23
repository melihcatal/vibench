import os

def get_config():
    return {
        'firebase': {
            'api_key': os.getenv('FIREBASE_API_KEY'),
            'auth_domain': os.getenv('FIREBASE_AUTH_DOMAIN')
        },
        'auth0': {
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
            'domain': os.getenv('AUTH0_DOMAIN')
        },
        'azure': {
            'client_id': os.getenv('AZURE_CLIENT_ID'),
            'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
            'authority': os.getenv('AZURE_AUTHORITY'),
            'scope': os.getenv('AZURE_SCOPE')
        }
    }