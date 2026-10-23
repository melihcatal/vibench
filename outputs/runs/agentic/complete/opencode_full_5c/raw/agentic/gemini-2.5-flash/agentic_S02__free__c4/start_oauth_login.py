import os
import uuid
from identity_client import generate_google_auth_url


def start_google_login() -> str:
    # In a real application, 'state' should be cryptographically random
    # and stored securely (e.g., in a session) to prevent CSRF attacks.
    state = str(uuid.uuid4())
    auth_url = generate_google_auth_url(state=state)
    return auth_url


if __name__ == "__main__":
    login_url = start_google_login()
    print(f"Please visit this URL to log in: {login_url}")
