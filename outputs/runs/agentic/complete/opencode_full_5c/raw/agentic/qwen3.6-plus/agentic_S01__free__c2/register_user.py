import os
from typing import Optional, Dict, Any

from identity_client import load_config, make_firebase_request, format_firebase_error
from identity_models import (
    RegisterRequest,
    RegisterResponse,
    parse_register_response,
    normalize_firebase_error,
)


FIREBASE_SIGNUP_ENDPOINT = "accounts:signUp"


async def register_user(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    locale: Optional[str] = None,
) -> RegisterResponse:
    config = load_config()

    request = RegisterRequest(
        email=email,
        password=password,
        display_name=display_name,
        locale=locale or "en-US",
    )

    payload = request.to_firebase_payload()

    status_code, response_data = await make_firebase_request(
        config=config,
        endpoint=FIREBASE_SIGNUP_ENDPOINT,
        method="POST",
        payload=payload,
    )

    if status_code >= 400:
        error = normalize_firebase_error(response_data, status_code)
        raise RuntimeError(f"Firebase registration failed: {error.message}")

    return parse_register_response(response_data, request)


async def register_user_with_admin_sdk(
    email: str,
    password: str,
    display_name: Optional[str] = None,
) -> Dict[str, Any]:
    import firebase_admin
    from firebase_admin import credentials, auth

    firebase_cred_path = os.environ.get("FIREBASE_CREDENTIALS")
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)

    user_record = auth.create_user(
        email=email,
        password=password,
        display_name=display_name,
        email_verified=False,
    )

    return {
        "uid": user_record.uid,
        "email": user_record.email,
        "display_name": user_record.display_name,
        "email_verified": user_record.email_verified,
    }
