import os
from typing import Optional, Dict, Any
import requests
from identity_models import (
    RegisterUserRequest,
    LoginRequest,
    RefreshRequest,
    PasswordResetRequest,
    AuthResponse,
    PasswordResetResponse,
    normalize_register_payload,
    normalize_login_payload,
    normalize_refresh_payload,
    normalize_password_reset_payload,
    parse_auth_response,
    parse_password_reset_response,
)


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.environ.get(
    "AUTH0_CONNECTION", "Username-Password-Authentication"
)
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")


def _get_base_url() -> str:
    domain = AUTH0_DOMAIN
    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")
    return f"https://{domain}"


def _make_request(
    method: str, endpoint: str, json_body: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    base_url = _get_base_url()
    url = f"{base_url}{endpoint}"
    headers = {"Content-Type": "application/json"}
    resp = requests.request(method, url, json=json_body, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def register_user(req: Optional[RegisterUserRequest] = None, **kwargs) -> AuthResponse:
    if req is None:
        req = RegisterUserRequest(
            email=kwargs["email"],
            password=kwargs["password"],
            connection=kwargs.get("connection", AUTH0_CONNECTION),
            given_name=kwargs.get("given_name"),
            family_name=kwargs.get("family_name"),
            metadata=kwargs.get("metadata"),
        )
    payload = normalize_register_payload(req)
    data = _make_request("POST", "/api/v2/users", payload)
    user_id = data.get("user_id", "")
    return AuthResponse(
        user_id=user_id,
        email=data.get("email", req.email),
        email_verified=data.get("email_verified", False),
        raw_response=data,
    )


def login_user(req: Optional[LoginRequest] = None, **kwargs) -> AuthResponse:
    if req is None:
        req = LoginRequest(
            email=kwargs["email"],
            password=kwargs["password"],
            connection=kwargs.get("connection", AUTH0_CONNECTION),
            audience=kwargs.get("audience", AUTH0_AUDIENCE),
            scope=kwargs.get("scope", "openid profile email"),
        )
    payload = normalize_login_payload(req, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
    data = _make_request("POST", "/oauth/token", payload)
    return parse_auth_response(data)


def refresh_access_token(
    req: Optional[RefreshRequest] = None, **kwargs
) -> AuthResponse:
    if req is None:
        req = RefreshRequest(
            refresh_token=kwargs["refresh_token"],
            client_id=kwargs.get("client_id", AUTH0_CLIENT_ID),
            audience=kwargs.get("audience", AUTH0_AUDIENCE),
        )
    payload = normalize_refresh_payload(req, AUTH0_CLIENT_SECRET)
    data = _make_request("POST", "/oauth/token", payload)
    return parse_auth_response(data)


def initiate_password_reset(
    req: Optional[PasswordResetRequest] = None, **kwargs
) -> PasswordResetResponse:
    if req is None:
        req = PasswordResetRequest(
            email=kwargs["email"],
            connection=kwargs.get("connection", AUTH0_CONNECTION),
        )
    payload = normalize_password_reset_payload(req, AUTH0_CLIENT_ID)
    data = _make_request("POST", "/dbconnections/change_password", payload)
    return parse_password_reset_response(data, req.email)
