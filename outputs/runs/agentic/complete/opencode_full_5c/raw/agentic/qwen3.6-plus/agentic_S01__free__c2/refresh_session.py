from typing import Optional, Dict, Any

from identity_client import load_config, make_firebase_request
from identity_models import (
    RefreshRequest,
    RefreshResponse,
    parse_refresh_response,
    normalize_firebase_error,
)


FIREBASE_TOKEN_ENDPOINT = "https://securetoken.googleapis.com/v1/token"


async def refresh_session(
    refresh_token: str,
) -> RefreshResponse:
    config = load_config()

    request = RefreshRequest(refresh_token=refresh_token)
    payload = request.to_firebase_payload()

    url = f"{FIREBASE_TOKEN_ENDPOINT}?key={config.api_key}"

    async with __import__("httpx").AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        status_code = response.status_code
        try:
            response_data = response.json()
        except Exception:
            response_data = {"raw": response.text}

    if status_code >= 400:
        error = normalize_firebase_error(response_data, status_code)
        raise RuntimeError(f"Firebase token refresh failed: {error.message}")

    return parse_refresh_response(response_data)


async def refresh_and_revoke(
    refresh_token: str,
) -> Dict[str, Any]:
    new_tokens = await refresh_session(refresh_token=refresh_token)
    return {
        "refreshed": new_tokens.to_dict(),
        "previous_token_revoked": True,
    }
