import os
import requests


def get_identity_client():
    domain_prefix = os.getenv('DOMAIN_PREFIX')
    region = os.getenv('REGION')
    domain = f'https://{domain_prefix}.auth.{region}.amazoncognito.com'
    return requests.Session()


def normalize_response(response):
    return response.json()