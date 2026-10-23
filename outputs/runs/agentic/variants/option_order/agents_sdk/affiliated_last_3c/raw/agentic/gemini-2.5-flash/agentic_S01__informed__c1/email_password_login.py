import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUTH_CLIENT_ID = os.getenv("AUTH0_AUTH_CLIENT_ID") # Auth API client ID
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE") # Audience for your API

def email_password_login(email, password):
    url = f"https://{{AUTH0_DOMAIN}}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": email,
        "password": password,
        "realm": "Username-Password-Authentication", # Use your database connection name
        "client_id": AUTH0_AUTH_CLIENT_ID,
        "audience": AUTH0_AUDIENCE,
        "scope": "openid profile email offline_access"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        tokens = response.json()
        return {
            "access_token": tokens.get("access_token"),
            "id_token": tokens.get("id_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in")
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "response": e.response.json() if e.response else None}

if __name__ == '__main__':
    # Example usage (requires AUTH0_DOMAIN, AUTH0_AUTH_CLIENT_ID, AUTH0_AUDIENCE environment variables)
    # print(email_password_login("test_user@example.com", "StrongPassword123!"))
    pass
