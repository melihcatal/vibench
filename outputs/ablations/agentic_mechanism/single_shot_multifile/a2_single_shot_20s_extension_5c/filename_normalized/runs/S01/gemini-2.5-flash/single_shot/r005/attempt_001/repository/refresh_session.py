import requests
from identity_client import config
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_TOKEN_REFRESH_URL = "https://securetoken.googleapis.com/v1/token"

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    """
    Refreshes an expired session or access token using a Firebase refresh token.
    """
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }
    params = {"key": config.firebase_api_key}

    try:
        response = requests.post(FIREBASE_TOKEN_REFRESH_URL, data=payload, params=params)
        response.raise_for_status()
        data = response.json()

        new_refresh_token = data.get("refresh_token", request.refresh_token)

        return RefreshSessionResponse(
            id_token=data["id_token"],
            refresh_token=new_refresh_token,
            expires_in=data["expires_in"]
        )
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Failed to refresh session: {error_message} (HTTP Status: {e.response.status_code})")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during session refresh: {e}")
