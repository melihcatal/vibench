from typing import Optional, Dict, Any

from identity_client import load_config, make_firebase_request
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    parse_password_reset_response,
    normalize_firebase_error,
)


FIREBASE_OOB_CODE_ENDPOINT = "accounts:sendOobCode"


async def password_reset(
    email: str,
    continue_url: Optional[str] = None,
    locale: Optional[str] = None,
) -> PasswordResetResponse:
    config = load_config()

    request = PasswordResetRequest(
        email=email,
        continue_url=continue_url,
        locale=locale or "en-US",
    )

    payload = request.to_firebase_payload()

    status_code, response_data = await make_firebase_request(
        config=config,
        endpoint=FIREBASE_OOB_CODE_ENDPOINT,
        method="POST",
        payload=payload,
    )

    if status_code >= 400:
        error = normalize_firebase_error(response_data, status_code)
        raise RuntimeError(f"Firebase password reset failed: {error.message}")

    return parse_password_reset_response(response_data, request)


async def password_reset_with_admin_sdk(
    email: str,
    continue_url: Optional[str] = None,
) -> Dict[str, Any]:
    import firebase_admin
    from firebase_admin import credentials, auth

    firebase_cred_path = __import__("os").environ.get("FIREBASE_CREDENTIALS")
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)

    action_link = auth.generate_password_reset_link(
        email=email,
        action_code_settings=auth.ActionCodeSettings(
            url=continue_url or "https://example.com/reset-complete",
            handle_code_in_app=True,
        ),
    )

    return {
        "email": email,
        "reset_link": action_link,
    }
