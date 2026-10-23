import os
import uuid
from identity_client import generate_google_auth_url


def start_oauth_login() -> str:
    # In a real application, 'state' should be stored securely (e.g., in a session)
    # and verified upon callback to prevent CSRF attacks.
    state = str(uuid.uuid4())

    # Example: print state to demonstrate, but do not expose in production logs.
    print(f"Generated state: {state}")  # Google-specific state for CSRF protection

    auth_url = generate_google_auth_url(state=state)
    return auth_url


if __name__ == "__main__":
    login_url = start_oauth_login()
    print(f"Please visit this URL to start the Google OAuth login: {login_url}")
