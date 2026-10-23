import os
import requests
from identity_client import get_auth0_management_api_token

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID") # Management API client ID
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET") # Management API client secret
AUTH0_MANAGEMENT_AUDIENCE = f"https://{{AUTH0_DOMAIN}}/api/v2/"

def register_user(email, password):
    access_token = get_auth0_management_api_token()
    if not access_token:
        return {"error": "Failed to get Auth0 Management API access token"}

    url = f"https://{{AUTH0_DOMAIN}}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {{access_token}}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication", # Use your database connection name
        "email_verified": False # User needs to verify their email
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        user_data = response.json()
        return {"user_id": user_data.get("user_id"), "email": user_data.get("email")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "response": e.response.json() if e.response else None}

if __name__ == '__main__':
    # Example usage (requires AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET environment variables)
    # print(register_user("test_user@example.com", "StrongPassword123!"))
    pass
