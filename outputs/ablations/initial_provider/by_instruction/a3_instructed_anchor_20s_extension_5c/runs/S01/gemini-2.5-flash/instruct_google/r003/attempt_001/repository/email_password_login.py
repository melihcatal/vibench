import requests
import os

class EmailPasswordLoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordLoginResponse:
    def __init__(self, id_token, refresh_token, expires_in, local_id):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.local_id = local_id

def email_password_login(request: EmailPasswordLoginRequest) -> EmailPasswordLoginResponse:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        return EmailPasswordLoginResponse(
            id_token=data.get("idToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=data.get("expiresIn"),
            local_id=data.get("localId")
        )
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during login: {e.response.text}")
        raise
    except Exception as e:
        print(f"Error during login: {e}")
        raise
