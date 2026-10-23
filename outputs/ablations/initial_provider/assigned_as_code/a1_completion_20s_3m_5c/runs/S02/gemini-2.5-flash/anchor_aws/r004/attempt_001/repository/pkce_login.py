import os
import requests
import json
import base64
import hashlib
from urllib.parse import urlencode

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def exchange_code_for_tokens_pkce(payload, config=None):
    config = config or {}
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    token_url = domain + "/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "redirect_uri": payload["redirect_uri"],
        "code": payload["code"],
        "code_verifier": payload["code_verifier"]
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=urlencode(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens with PKCE: {e}")
        return None
