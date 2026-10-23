import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app

def register_user(email: str, password: str):
    app = get_firebase_app()
    try:
        user = auth.create_user(
            email=email,
            password=password,
            app=app
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")

if __name__ == '__main__':
    # Example usage (will not run in production, just for demonstration)
    # import os
    # if not firebase_admin._apps:
    #     firebase_admin.initialize_app(
    #         credential=firebase_admin.credentials.ApplicationDefault(),
    #         name='default' # Or a specific name
    #     )
    # try:
    #     user_info = register_user("test_user@example.com", "securePassword123!")
    #     print(f"User registered: {user_info}")
    # except RuntimeError as e:
    #     print(f"Error: {e}")
    pass
