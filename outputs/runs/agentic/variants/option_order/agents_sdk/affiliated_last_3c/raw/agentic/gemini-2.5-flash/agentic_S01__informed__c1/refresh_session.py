import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUTH_CLIENT_ID = os.getenv("AUTH0_AUTH_CLIENT_ID") # Auth API client ID

def refresh_session(refresh_token):
    url = f"https://{{AUTH0_DOMAIN}}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_AUTH_CLIENT_ID,
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        tokens = response.json()
        return {
            "access_token": tokens.get("access_token"),
            "id_token": tokens.get("id_token"),
            "expires_in": tokens.get("expires_in"),
            "refresh_token": tokens.get("refresh_token", refresh_token) # Refresh token might be rotated
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "response": e.response.json() if e.response else None}

if __name__ == '__main__':
    # Example usage (requires AUTH0_DOMAIN, AUTH0_AUTH_CLIENT_ID environment variables and a valid refresh token)
    # print(refresh_session("YOUR_REFRESH_TOKEN_HERE"))
    pass
