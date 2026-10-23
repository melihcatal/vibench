from identity_client import get_firebase_auth_client

def send_password_reset_email(email: str) -> str:
    """
    Generates and sends a password reset link to the user's email.
    Note: Firebase Admin SDK generates the link, sending the email must be
    handled separately or configured in the Firebase console.

    Args:
        email: The email address of the user to send a reset link to.

    Returns:
        The generated password reset link.
    """
    auth_client = get_firebase_auth_client()
    try:
        link = auth_client.generate_password_reset_link(email)
        print(f"Password reset link generated for {email}.")
        # In a real app, you would use an email service to send this link.
        return link
    except Exception as e:
        print(f"Error generating password reset link: {e}")
        raise
