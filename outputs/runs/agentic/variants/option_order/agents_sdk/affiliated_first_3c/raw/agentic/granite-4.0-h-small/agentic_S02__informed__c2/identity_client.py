import os
import json
import requests

# Helper client for Google Identity Platform OIDC
# GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI must be set

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')


class IdentityClient:
    def __init__(self):
        pass

    def start_oauth_flow(self):
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?"
        auth_url += f"response_type=code&"
        auth_url += f"client_id={GOOGLE_CLIENT_ID}&"
        auth_url += f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        auth_url += "scope=openid%20email%20profile&"
        auth_url += "access_type=offline&"
        auth_url += "prompt=consent"
        print('Open the URL in a browser to begin login:')
        print(auth_url)
        # Simple local server could be launched here or handled elsewhere
        return auth_url

    def exchange_code(self, code):
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        return resp.json()

    def fetch_user_profile(self, id_token):
        payload = self._decode_token(id_token)
        profile = {
            'sub': payload.get('sub'),
            'email': payload.get('email'),
            'email_verified': payload.get('email_verified'),
            'name': payload.get('name'),
            'given_name': payload.get('given_name'),
            'family_name': payload.get('family_name'),
            'picture': payload.get('picture'),
            'locale': payload.get('locale')
        }
        return profile

    def _decode_token(self, token):
        # Minimal verification for demonstration
        import jwt, base64, hashlib
        payload = jwt.decode(token, options={"verify_signature": False})
        if payload.get('aud') != GOOGLE_CLIENT_ID:
            raise ValueError('Audience mismatch')
        return payload

if __name__ == '__main__':
    client = IdentityClient()
    auth_url = client.start_oauth_flow()
    # Further steps would capture callback and continue
