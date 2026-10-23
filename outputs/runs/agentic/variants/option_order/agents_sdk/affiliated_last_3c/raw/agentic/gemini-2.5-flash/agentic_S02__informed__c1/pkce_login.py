import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
import json
from identity_client import get_google_oidc_config

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def start_google_pkce_flow():
    config = get_google_oidc_config()
    client_id = config["GOOGLE_CLIENT_ID"]
    redirect_uri = config["GOOGLE_REDIRECT_URI"]
    discovery_url = config["GOOGLE_DISCOVERY_URL"]

    # Fetch discovery document to get authorization endpoint
    try:
        discovery_response = requests.get(discovery_url)
        discovery_response.raise_for_status()
        discovery_doc = discovery_response.json()
        authorization_endpoint = discovery_doc["authorization_endpoint"]
        token_endpoint = discovery_doc["token_endpoint"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google OIDC discovery document: {e}")
        return None, None, None

    code_verifier, code_challenge = generate_pkce_challenge()

    scope = "openid profile email"
    response_type = "code"
    code_challenge_method = "S256"

    auth_url = (
        f"{authorization_endpoint}?"
        f"response_type={response_type}&"
        f"client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote_plus(redirect_uri)}&"
        f"scope={urllib.parse.quote_plus(scope)}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method={code_challenge_method}"
    )

    print(f"Redirect user to: {auth_url}")
    return auth_url, code_verifier, token_endpoint

def exchange_code_for_tokens_pkce(authorization_code: str, code_verifier: str, token_endpoint: str):
    config = get_google_oidc_config()
    client_id = config["GOOGLE_CLIENT_ID"]
    redirect_uri = config["GOOGLE_REDIRECT_URI"]

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    try:
        response = requests.post(token_endpoint, headers=headers, data=payload)
        response.raise_for_status()
        tokens = response.json()
        print("Successfully exchanged code for tokens using PKCE.")
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens with PKCE: {e}")
        return None

if __name__ == "__main__":
    auth_url, verifier, token_endpoint = start_google_pkce_flow()
    if auth_url:
        print(f"Please visit the URL to authorize and get the authorization code.")
        print(f"Store this code_verifier for the next step: {verifier}")

        # Simulate receiving an authorization code from the redirect
        # For a real application, this would come from the redirect URI handler
        sample_auth_code = os.environ.get("GOOGLE_SAMPLE_AUTH_CODE", "dummy_auth_code_from_redirect")
        if sample_auth_code != "dummy_auth_code_from_redirect" and verifier and token_endpoint:
            print("\nAttempting to exchange code for tokens...")
            tokens = exchange_code_for_tokens_pkce(sample_auth_code, verifier, token_endpoint)
            if tokens:
                print(json.dumps(tokens, indent=2))
        else:
            print("To complete the flow, set GOOGLE_SAMPLE_AUTH_CODE and run again after authorization.")
