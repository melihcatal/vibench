import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_MANAGEMENT_API_AUDIENCE = f"https://{AUTH0_DOMAIN}/api/v2/"


def get_management_api_token():
    """
    Obtains a Management API access token using the Client Credentials Flow.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_MANAGEMENT_API_AUDIENCE,
        "grant_type": "client_credentials",
    }
    response = requests.post(token_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("access_token")
