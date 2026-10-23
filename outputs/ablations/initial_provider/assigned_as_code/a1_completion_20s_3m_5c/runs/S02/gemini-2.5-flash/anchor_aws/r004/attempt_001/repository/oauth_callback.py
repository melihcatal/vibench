import os
import requests
import json
from urllib.parse import urlencode

def exchange_code_for_tokens(payload, config=None):
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
        "code": payload["code"]
    }
    
    # If client_secret is provided, include it for confidential clients
    if config.get("client_secret"):
        data["client_secret"] = config["client_secret"]

    try:
        response = requests.post(token_url, headers=headers, data=urlencode(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return None
