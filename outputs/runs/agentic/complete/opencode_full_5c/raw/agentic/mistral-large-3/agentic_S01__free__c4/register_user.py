from firebase_admin import auth, initialize_app
from firebase_admin.auth import EmailAlreadyExistsError
from identity_models import RegisterUserRequest, RegisterUserResponse
import os

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(options={"projectId": os.getenv("FIREBASE_PROJECT_ID")})


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
            disabled=False,
        )
        return RegisterUserResponse(
            success=True, user_id=user.uid, email_verified=user.email_verified
        )
    except EmailAlreadyExistsError:
        return RegisterUserResponse(success=False, error="Email already exists")
    except Exception as e:
        return RegisterUserResponse(success=False, error=str(e))
