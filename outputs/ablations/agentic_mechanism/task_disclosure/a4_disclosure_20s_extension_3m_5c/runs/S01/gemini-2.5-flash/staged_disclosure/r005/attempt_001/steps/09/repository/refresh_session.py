import os
import requests
import json

# Replace with your Auth0 domain and client ID
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_REFRESH_TOKEN = os.environ.get("AUTH0_REFRESH_TOKEN", "YOUR_AUTH0_REFRESH_TOKEN")

def refresh_auth0_token(refresh_token: str):
    """
    Refreshes an Auth0 access token using a refresh token.

    Args:
        refresh_token: The refresh token obtained during the initial login.

    Returns:
        A dictionary containing the new access token, ID token, and other
        relevant information, or None if the refresh fails.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(token_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response content: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

if __name__ == "__main__":
    if not AUTH0_REFRESH_TOKEN or AUTH0_REFRESH_TOKEN == "YOUR_AUTH0_REFRESH_TOKEN":
        print("Please set the AUTH0_REFRESH_TOKEN environment variable or replace the placeholder.")
    else:
        print(f"Attempting to refresh token using Auth0 Domain: {AUTH0_DOMAIN}, Client ID: {AUTH0_CLIENT_ID}")
        new_tokens = refresh_auth0_token(AUTH0_REFRESH_TOKEN)

        if new_tokens:
            print("Token refresh successful!")
            print(f"New Access Token: {new_tokens.get('access_token', 'N/A')}")
            print(f"New ID Token: {new_tokens.get('id_token', 'N/A')}")
            print(f"Expires In: {new_tokens.get('expires_in', 'N/A')} seconds")
        else:
            print("Token refresh failed.")
