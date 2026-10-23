import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app

def password_reset(email: str):
    app = get_firebase_app()
    try:
        link = auth.generate_password_reset_link(email, app=app)
        return {"status": "success", "reset_link": link}
    except Exception as e:
        raise RuntimeError(f"Failed to generate password reset link for {email}: {e}")

if __name__ == '__main__':
    # Example usage: Will generate a password reset link for the given email.
    # from dotenv import load_dotenv
    # import os
    # load_dotenv()
    # if not firebase_admin._apps:
    #     firebase_admin.initialize_app(
    #         credential=firebase_admin.credentials.ApplicationDefault(),
    #         name='default'
    #     )
    # try:
    #     reset_info = password_reset("test_user@example.com")
    #     print(f"Password reset initiated: {reset_info}")
    # except RuntimeError as e:
    #     print(f"Error: {e}")
    pass
