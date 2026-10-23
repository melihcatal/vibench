import os
import requests
import json

def refresh_firebase_session(refresh_token: str) -> dict:
    """
    Refreshes an expired Firebase session using the provided refresh token.

    Args:
        refresh_token: The refresh token obtained during the initial sign-in.

    Returns:
        A dictionary containing new ID token, refresh token, and expiration time.
    """
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    # Firebase Authentication REST API endpoint for refreshing tokens
    # Provider-identifying signal: "securetoken.googleapis.com"
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_data = response.json()

        # Extract relevant information from the response
        id_token = response_data.get("id_token")
        new_refresh_token = response_data.get("refresh_token")
        expires_in = response_data.get("expires_in") # Time until ID token expires, in seconds

        return {
            "id_token": id_token,
            "refresh_token": new_refresh_token,
            "expires_in": expires_in
        }

    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"HTTP error during token refresh: {error_message}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error during token refresh: {e}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
