import requests
from identity_client import get_firebase_web_api_key
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_SECURETOKEN_REST_API = "https://securetoken.googleapis.com/v1/token"

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    api_key = get_firebase_web_api_key()
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request['refresh_token']
    }
    try:
        response = requests.post(f"{FIREBASE_SECURETOKEN_REST_API}?key={api_key}", json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "id_token": data['id_token'],
            "refresh_token": data['refresh_token'],
            "expires_in": str(data['expires_in'])
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to refresh session: {e}, Response: {getattr(e.response, 'text', 'No response text')}")

