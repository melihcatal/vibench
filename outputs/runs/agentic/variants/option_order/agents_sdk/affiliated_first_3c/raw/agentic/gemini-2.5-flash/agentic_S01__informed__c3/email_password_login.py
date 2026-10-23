import requests
from identity_client import identity_client
from identity_models import UserLogin, AuthTokens

def email_password_login(user_login: UserLogin) -> AuthTokens:
    url = f"{identity_client.rest_api_base_url}/accounts:signInWithPassword?key={identity_client.firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": user_login.email,
        "password": user_login.password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        return AuthTokens(
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=int(data["expiresIn"]),
            local_id=data["localId"]
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to login user: {e}")
