import requests
from identity_client import identity_client
from identity_models import AuthTokens

def refresh_session(refresh_token: str) -> AuthTokens:
    url = f"{identity_client.securetoken_api_base_url}/token?key={identity_client.firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        return AuthTokens(
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
            expires_in=int(data["expires_in"]),
            local_id=data.get("user_id", "") # user_id is not always returned for refresh
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to refresh session: {e}")
