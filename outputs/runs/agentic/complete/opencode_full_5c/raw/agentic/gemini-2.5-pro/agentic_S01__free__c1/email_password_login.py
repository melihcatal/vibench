import os
import requests
from identity_models import UserLogin, LoginResponse


def sign_in_with_email_password(user_login: UserLogin) -> dict:
    api_key = os.environ.get("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": user_login.email,
        "password": user_login.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        login_response = LoginResponse.parse_obj(response.json())
        return login_response.dict()
    else:
        return {"error": response.json().get("error", "Unknown error")}
