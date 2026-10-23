import os
import boto3
import base64
import json
import requests

COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
COGNITO_USER_POOL_CLIENT_ID = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")
COGNITO_USER_POOL_CLIENT_SECRET = os.environ.get("COGNITO_USER_POOL_CLIENT_SECRET")
COGNITO_REDIRECT_URI = os.environ.get("COGNITO_REDIRECT_URI")
COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")

def exchange_code_for_tokens(authorization_code: str):
    """
    Exchanges an authorization code for ID, access, and refresh tokens using AWS Cognito.
    """
    if not all([COGNITO_DOMAIN, COGNITO_USER_POOL_CLIENT_ID, COGNITO_REDIRECT_URI]):
        raise ValueError("Missing one or more Cognito environment variables.")

    token_endpoint = f"https://{COGNITO_DOMAIN}/oauth2/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "client_id": COGNITO_USER_POOL_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": COGNITO_REDIRECT_URI,
    }
    
    if COGNITO_USER_POOL_CLIENT_SECRET:
        client_secret_bytes = f"{COGNITO_USER_POOL_CLIENT_ID}:{COGNITO_USER_POOL_CLIENT_SECRET}".encode("utf-8")
        base64_auth = base64.b64encode(client_secret_bytes).decode("utf-8")
        headers["Authorization"] = f"Basic {base64_auth}"

    try:
        response = requests.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage (in a real application, the code would come from the redirect URL)
    example_code = "YOUR_AUTHORIZATION_CODE_HERE"
    try:
        user_tokens = exchange_code_for_tokens(example_code)
        print("Successfully exchanged code for tokens:")
        print(json.dumps(user_tokens, indent=2))
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
