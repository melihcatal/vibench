import os
import requests

def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using Google Identity Platform (Firebase Authentication).
    """
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")
        raise

