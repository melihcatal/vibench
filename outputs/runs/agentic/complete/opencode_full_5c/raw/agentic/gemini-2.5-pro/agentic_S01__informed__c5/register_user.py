from firebase_admin import auth
from identity_client import initialize_firebase_admin
from identity_models import UserRegistrationRequest


def register_new_user(user_details: UserRegistrationRequest):
    """
    Creates a new user in Firebase Authentication.
    """
    initialize_firebase_admin()
    try:
        user = auth.create_user(
            email=user_details.email,
            password=user_details.password,
            display_name=user_details.display_name,
            email_verified=False,
        )
        return {"uid": user.uid, "message": "Successfully created new user"}
    except Exception as e:
        # Handle exceptions, e.g., email already exists
        return {"error": str(e)}
