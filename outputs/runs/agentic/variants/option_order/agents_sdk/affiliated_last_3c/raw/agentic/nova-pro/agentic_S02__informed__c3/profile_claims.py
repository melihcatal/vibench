import os
from google.oauth2 import id_token
from google.auth.transport import requests

def get_profile_claims(id_token):
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    claims = id_token.verify_token(id_token, requests.Request(), audience=client_id)
    return claims

if __name__ == '__main__':
    id_token = 'your_id_token'
    print(get_profile_claims(id_token)