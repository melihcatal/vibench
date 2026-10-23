"""Register a new email/password user account using Firebase Authentication."""

import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from identity_client import get_firebase_app
from identity_models import RegisterRequest, RegisterResponse, normalize_register_response


def register_user(request: RegisterRequest) -> RegisterResponse:
    """Create a new user account with email and password via Firebase Authentication.

    Uses the Firebase Admin SDK to create a user in the Firebase Authentication
    user pool with the provided email, password, and optional display name.

    Args:
        request: RegisterRequest containing email, password, and optional display_name.

    Returns:
        RegisterResponse with uid, email, creation timestamp, and display_name.
    """
    app = get_firebase_app()

    create_kwargs = {
        "email": request.email,
        "password": request.password,
        "app": app,
    }

    if request.display_name:
        create_kwargs["display_name"] = request.display_name

    try:
        user_record = firebase_auth.create_user(**create_kwargs)
        return normalize_register_response(user_record)
    except firebase_auth.EmailAlreadyExistsError as e:
        raise ValueError(f"Email already registered: {request.email}") from e
    except firebase_auth.InvalidEmailError as e:
        raise ValueError(f"Invalid email format: {request.email}") from e
    except firebase_auth.WeakPasswordError as e:
        raise ValueError("Password does not meet Firebase strength requirements") from e
