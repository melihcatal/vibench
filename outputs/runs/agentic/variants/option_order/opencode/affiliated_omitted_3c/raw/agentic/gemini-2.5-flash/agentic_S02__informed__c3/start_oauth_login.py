import os
import uuid
from identity_client import Auth0Client


def start_login() -> str:
    """Starts an OAuth or OIDC authorization-code login flow."""
    client = Auth0Client()
    state = str(uuid.uuid4())  # For CSRF protection
    # In a real application, 'state' would be stored in a session for validation on callback.

    return client.get_authorize_url(state=state)


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     # Set environment variables for demonstration
#     os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
#     os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
#     os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
#     auth_url = start_login()
#     print(f"Redirect to: {auth_url}")
