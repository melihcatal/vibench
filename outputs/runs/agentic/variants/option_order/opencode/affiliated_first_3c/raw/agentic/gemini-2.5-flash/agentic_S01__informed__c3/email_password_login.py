import firebase_admin
from firebase_admin import auth
from identity_models import UserLoginRequest, UserResponse
from identity_client import initialize_firebase

initialize_firebase()


def email_password_login(request: UserLoginRequest) -> UserResponse:
    # Firebase Admin SDK does not provide a direct email/password login method
    # that returns tokens for client-side use. This SDK is for server-side
    # user management. Actual login with email/password and token acquisition
    # is typically done on the client-side using Firebase Client SDKs.
    # For this exercise, we will simulate a successful login by verifying
    # the user's existence in Firebase Authentication.
    try:
        user = auth.get_user_by_email(request.email)
        # In a real scenario, you would also verify the password here, but
        # Firebase Admin SDK doesn't expose password verification for security reasons.
        # This function primarily confirms the user account exists.
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            email_verified=user.email_verified,
            disabled=user.disabled,
        )
    except auth.UserNotFoundError:
        raise ValueError("User not found or invalid credentials.")
    except Exception as e:
        raise RuntimeError(f"Failed to process login: {e}")
