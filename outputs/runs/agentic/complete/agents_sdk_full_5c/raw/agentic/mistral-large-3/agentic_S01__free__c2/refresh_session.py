import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    try:
        # Firebase REST API for token refresh
        rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={os.getenv('FIREBASE_API_KEY')}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": request.refresh_token
        }
        response = requests.post(rest_api_url, data=payload)
        response.raise_for_status()
        data = response.json()
        
        return RefreshSessionResponse(
            success=True,
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
            expires_in=int(data["expires_in"])
        )
    except requests.exceptions.RequestException as e:
        return RefreshSessionResponse(
            success=False,
            error_message=str(e)
        )