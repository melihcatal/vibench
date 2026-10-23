import os
import json
import logging
from typing import Optional, Dict, Any, Tuple

import requests
from requests.exceptions import RequestException

from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    IdentityError,
)

logger = logging.getLogger(__name__)

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_MANAGEMENT_API_TOKEN = os.environ.get("AUTH0_MANAGEMENT_API_TOKEN", "")

AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_API_URL = f"{AUTH0_BASE_URL}/api/v2"
AUTH0_OAUTH_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_management_api_headers() -> Dict[str, str]:
    headers = DEFAULT_HEADERS.copy()
    if AUTH0_MANAGEMENT_API_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH0_MANAGEMENT_API_TOKEN}"
    return headers


def get_oauth_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
    }


def make_auth0_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Tuple[Optional[Dict[str, Any]], Optional[IdentityError]]:
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json(), None
    except RequestException as exc:
        status_code = getattr(exc.response, "status_code", 0) if exc.response else 0
        try:
            error_body = exc.response.json() if exc.response is not None else {}
        except (ValueError, AttributeError):
            error_body = {}
        error = IdentityError(
            status_code=status_code,
            error=error_body.get("error", str(exc)),
            error_description=error_body.get("error_description", str(exc)),
            raw_response=error_body,
        )
        logger.error("Auth0 request failed: %s", error)
        return None, error


def register_user(
    request: RegisterUserRequest,
) -> Tuple[Optional[RegisterUserResponse], Optional[IdentityError]]:
    url = f"{AUTH0_API_URL}/users"
    headers = get_management_api_headers()
    payload = request.to_auth0_payload()
    data, error = make_auth0_request("POST", url, headers, payload)
    if error:
        return None, error
    return RegisterUserResponse.from_auth0_response(data), None


def login_user(
    request: LoginRequest,
) -> Tuple[Optional[LoginResponse], Optional[IdentityError]]:
    url = AUTH0_OAUTH_TOKEN_URL
    headers = get_oauth_headers()
    payload = request.to_auth0_payload()
    data, error = make_auth0_request("POST", url, headers, payload)
    if error:
        return None, error
    return LoginResponse.from_auth0_response(data), None


def refresh_token(
    request: RefreshTokenRequest,
) -> Tuple[Optional[RefreshTokenResponse], Optional[IdentityError]]:
    url = AUTH0_OAUTH_TOKEN_URL
    headers = get_oauth_headers()
    payload = request.to_auth0_payload()
    data, error = make_auth0_request("POST", url, headers, payload)
    if error:
        return None, error
    return RefreshTokenResponse.from_auth0_response(data), None


def initiate_password_reset(
    request: PasswordResetRequest,
) -> Tuple[Optional[PasswordResetResponse], Optional[IdentityError]]:
    url = f"{AUTH0_BASE_URL}/dbconnections/change_password"
    headers = get_oauth_headers()
    payload = request.to_auth0_payload()
    data, error = make_auth0_request("POST", url, headers, payload)
    if error:
        return None, error
    return PasswordResetResponse.from_auth0_response(data), None
