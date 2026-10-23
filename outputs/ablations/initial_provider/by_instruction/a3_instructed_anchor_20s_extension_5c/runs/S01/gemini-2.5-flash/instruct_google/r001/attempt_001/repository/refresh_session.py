import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import refresh_token_request

FIREBASE_REFRESH_TOKEN_API_URL = "https://securetoken.googleapis.com/v1/token?key=" + FIREBASE_WEB_API_KEY

def refresh_session(refresh_token):
    """
    Refreshes an expired session or access token using the Firebase Authentication REST API.
    """
    payload = refresh_token_request(refresh_token)
    try:
        response = requests.post(FIREBASE_REFRESH_TOKEN_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to refresh token."}
