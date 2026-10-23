from typing import Optional, Dict, Any

from identity_client import load_config, make_firebase_request, verify_id_token
from identity_models import (
    LoginRequest,
    LoginResponse,
    parse_login_response,
    normalize_firebase_error,
)


FIREBASE_SIGNIN_ENDPOINT = "accounts:signInWithPassword"


async def email_password_login(
    email: str,
    password: str,
) -> LoginResponse:
    config = load_config()

    request = LoginRequest(email=email, password=password)
    payload = request.to_firebase_payload()

    status_code, response_data = await make_firebase_request(
        config=config,
        endpoint=FIREBASE_SIGNIN_ENDPOINT,
        method="POST",
        payload=payload,
    )

    if status_code >= 400:
        error = normalize_firebase_error(response_data, status_code)
        raise RuntimeError(f"Firebase login failed: {error.message}")

    return parse_login_response(response_data, request)


async def login_and_verify_token(
    email: str,
    password: str,
) -> Dict[str, Any]:
    login_result = await email_password_login(email=email, password=password)

    config = load_config()
    token_info = await verify_id_token(config, login_result.id_token)

    return {
        "login": login_result.to_dict(),
        "token_info": token_info,
    }
