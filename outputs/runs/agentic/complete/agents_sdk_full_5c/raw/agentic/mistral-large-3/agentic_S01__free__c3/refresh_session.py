import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse, RefreshSessionError


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://securetoken.googleapis.com/v1/token?key={firebase_api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }

    response = requests.post(url, data=payload)
    data = response.json()

    if response.status_code == 200:
        return RefreshSessionResponse(
            success=True,
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"]
        )
    else:
        return RefreshSessionResponse(
            success=False,
            error=RefreshSessionError(
                code=data.get("error", {}).get("code"),
                message=data.get("error", {}).get("message")
            )
        )