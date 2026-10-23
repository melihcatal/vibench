import os
import requests
from identity_models import LoginRequest, LoginResponse

# Firebase Auth REST API Endpoint (for email/password sign-in which requires API Key)
# The Firebase Admin SDK does not directly support email/password sign-in to get ID tokens client-side,
# so we use the REST API for this specific flow.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

def email_password_login(request: LoginRequest) -> LoginResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(FIREBASE_AUTH_SIGNIN_URL, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return LoginResponse(
            id_token=data.get("idToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=int(data.get("expiresIn", 0)),
            uid=data.get("localId")
        )
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Failed to login: {error_message}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during login: {e}")

if __name__ == '__main_':
    # This block is for demonstration/testing only
    # os.environ["FIREBASE_WEB_API_KEY"] = "YOUR_FIREBASE_WEB_API_KEY"
    # try:
    #     login_req = LoginRequest(email="test@example.com", password="StrongPassword123!")
    #     login_res = email_password_login(login_req)
    #     print(f"Login successful. User ID: {login_res.uid}, ID Token (truncated): {login_res.id_token[:30]}...")
    # except RuntimeError as e:
    #     print(f"Login error: {e}")
    pass
