import requests
import os
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in a user with email and password using Firebase Authentication REST API."""
    try:
        # Firebase API key from environment
        api_key = os.environ.get("FIREBASE_API_KEY")
        if not api_key:
            raise ValueError("FIREBASE_API_KEY environment variable is required")

        # Firebase Authentication REST API endpoint
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        # Prepare request payload
        payload = {"email": email, "password": password, "returnSecureToken": True}

        # Make API call to Firebase
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        # Extract tokens and user info
        id_token = data.get("idToken")
        refresh_token = data.get("refreshToken")
        local_id = data.get("localId")
        email = data.get("email")
        display_name = data.get("displayName")

        if not id_token:
            raise ValueError("No authentication token received from Firebase")

        # Return normalized response
        return LoginResponse(
            user_id=local_id,
            email=email,
            display_name=display_name,
            access_token=id_token,
            refresh_token=refresh_token,
            expires_in=data.get("expiresIn", 3600),
            token_type="Bearer",
            provider="firebase",
        )
    except requests.exceptions.RequestException as e:
        if e.response and e.response.status_code == 400:
            error_data = e.response.json()
            error_msg = error_data.get("error", {}).get(
                "message", "Invalid credentials"
            )
            if "INVALID_PASSWORD" in error_msg or "EMAIL_NOT_FOUND" in error_msg:
                raise ValueError("Invalid email or password")
        raise RuntimeError(f"Login failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Login failed: {str(e)}")
