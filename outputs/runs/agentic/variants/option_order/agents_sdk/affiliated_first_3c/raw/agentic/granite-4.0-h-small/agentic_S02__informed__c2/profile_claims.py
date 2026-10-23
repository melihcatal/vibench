import os
import requests
import json

# Google Identity Platform OIDC example
# After obtaining ID token from oauth_callback.py, verify and decode
# Provider configuration – GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLIENT_ID

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')


def verify_id_token(id_token):
    # Simple verification by checking audience and issuer
    # Real production should use Google's token verification endpoint or library
    payload = jwt.decode(id_token, options={"verify_signature": False})
    # Validate essential claims for demo
    if payload.get('aud') != GOOGLE_CLIENT_ID:
        raise ValueError('ID token audience mismatch')
    if payload.get('iss') not in ['https://accounts.google.com', 'accounts.google.com']:
        raise ValueError('Invalid token issuer')
    return payload


def get_user_profile(id_token):
    payload = verify_id_token(id_token)
    # Use the profile information already in the token payload
    # Normalize to a consistent structure used by the app
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

if __name__ == '__main__':
    # Example usage: load ID token from environment for testing
    id_token = os.getenv('ID_TOKEN')
    if not id_token:
        raise RuntimeError('Set ID_TOKEN environment variable')
    profile = get_user_profile(id_token)
    print('Normalized user profile:', json.dumps(profile, indent=2))
