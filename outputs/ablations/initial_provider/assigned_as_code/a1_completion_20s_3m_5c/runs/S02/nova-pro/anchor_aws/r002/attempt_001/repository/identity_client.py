import os
import requests


def get_identity_client(config):
    return requests.Session()


def load_identity_config():
    return {
        'domain_prefix': os.getenv('IDENTITY_DOMAIN_PREFIX'),
        'region': os.getenv('IDENTITY_REGION'),
        'client_id': os.getenv('IDENTITY_CLIENT_ID'),
        'client_secret': os.getenv('IDENTITY_CLIENT_SECRET'),
        'redirect_uri': os.getenv('IDENTITY_REDIRECT_URI')
    }