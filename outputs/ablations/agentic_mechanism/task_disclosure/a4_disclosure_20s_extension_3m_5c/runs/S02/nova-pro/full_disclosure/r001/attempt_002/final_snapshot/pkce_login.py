import requests
import base64
import hashlib
import random

AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
CLIENT_ID = 'your-auth0-client-id'
REDIRECT_URI = 'https://your-app.com/callback'

def generate_code_verifier():
    # Generate a random string of bytes
    code_verifier = ''.join(random.choices('abcdef0123456789', k=32))
    return code_verifier

def generate_code_challenge(code_verifier):
    # Create a SHA-256 hash of the code_verifier
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')