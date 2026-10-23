
import os
from auth0.management import Auth0

def start_password_reset(email: str, connection_name: str = "Username-Password-Authentication"):
    """
    Starts a password reset flow for a local account using Auth0.

    Args:
        email (str): The email address of the user requesting a password reset.
        connection_name (str): The name of the Auth0 connection to use.
                               Defaults to "Username-Password-Authentication".

    Returns:
        dict: A dictionary indicating the success or failure of the password reset initiation.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_MANAGEMENT_CLIENT_ID = os.environ.get("AUTH0_MANAGEMENT_CLIENT_ID")
    AUTH0_MANAGEMENT_CLIENT_SECRET = os.environ.get("AUTH0_MANAGEMENT_CLIENT_SECRET")

    if not all([AUTH0_DOMAIN, AUTH0_MANAGEMENT_CLIENT_ID, AUTH0_MANAGEMENT_CLIENT_SECRET]):
        return {"success": False, "message": "Auth0 environment variables are not set."}

    try:
        management_api = Auth0(AUTH0_DOMAIN, AUTH0_MANAGEMENT_CLIENT_ID, AUTH0_MANAGEMENT_CLIENT_SECRET)
        management_api.users.change_password(
            user_id="",  # Not required for this method, email is used
            email=email,
            connection=connection_name
        )
        return {"success": True, "message": f"Password reset email sent to {email}."}
    except Exception as e:
        return {"success": False, "message": f"Failed to initiate password reset: {e}"}

