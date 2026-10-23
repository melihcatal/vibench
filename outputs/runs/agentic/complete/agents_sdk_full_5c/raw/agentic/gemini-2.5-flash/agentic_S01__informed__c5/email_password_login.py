import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app

def email_password_login(id_token: str):
    # For Firebase, actual email/password login happens client-side.
    # This server-side integration step can verify the ID token received from the client.
    app = get_firebase_app()
    try:
        decoded_token = auth.verify_id_token(id_token, app=app)
        # If the token is valid, it means the user successfully logged in.
        # The decoded_token contains user information.
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token["email"],
            "decoded_token": decoded_token
        }
    except Exception as e:
        raise RuntimeError(f"Failed to verify ID token: {e}")

if __name__ == '__main__':
    # Example usage: Requires a valid ID token obtained from a client-side Firebase login.
    # from dotenv import load_dotenv
    # import os
    # load_dotenv()
    # if not firebase_admin._apps:
    #     firebase_admin.initialize_app(
    #         credential=firebase_admin.credentials.ApplicationDefault(),
    #         name='default'
    #     )
    # try:
    #     # Replace with a real ID token for testing
    #     test_id_token = "YOUR_FIREBASE_CLIENT_ID_TOKEN"
    #     user_session = email_password_login(test_id_token)
    #     print(f"User logged in (token verified): {user_session}")
    # except RuntimeError as e:
    #     print(f"Error: {e}")
    pass
