import requests
import os

class RefreshSessionRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class RefreshSessionResponse:
    def __init__(self, id_token: str, refresh_token: str, expires_in: str):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        return RefreshSessionResponse(
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in")
        )
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during token refresh: {e.response.text}")
        raise
    except Exception as e:
        print(f"Error during token refresh: {e}")
        raise
