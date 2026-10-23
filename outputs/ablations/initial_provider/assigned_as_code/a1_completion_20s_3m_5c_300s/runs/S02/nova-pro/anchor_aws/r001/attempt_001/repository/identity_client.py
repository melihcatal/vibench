import requests


def get_cognito_client(config):
    return requests.Session()


def get_cognito_config():
    return {
        'domain_prefix': 'your-cognito-domain-prefix',
        'region': 'your-cognito-region',
        'client_id': 'your-cognito-client-id'
    }