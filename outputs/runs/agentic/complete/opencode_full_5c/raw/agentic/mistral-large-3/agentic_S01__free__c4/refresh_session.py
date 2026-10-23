import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse
import os


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    refresh_url = f"https://securetoken.googleapis.com/v1/token?key={os.getenv('FIREBASE_API_KEY')}"
    payload = {"grant_type": "refresh_token", "refresh_token": request.refresh_token}
    response = requests.post(refresh_url, data=payload)

    if response.status_code == 200:
        data = response.json()
        return RefreshSessionResponse(
            success=True,
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            refresh_token=data.get("refresh_token", request.refresh_token),
        )
    else:
        return RefreshSessionResponse(
            success=False,
            error=response.json().get("error", {}).get("message", "Refresh failed"),
        )
