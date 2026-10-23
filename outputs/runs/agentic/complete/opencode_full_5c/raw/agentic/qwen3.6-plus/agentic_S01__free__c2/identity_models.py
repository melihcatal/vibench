from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


@dataclass
class RegisterRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = "en-US"
    custom_claims: Optional[Dict[str, Any]] = None

    def to_firebase_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email.strip().lower(),
            "password": self.password,
            "emailVerified": False,
        }
        if self.display_name:
            payload["displayName"] = self.display_name.strip()
        return payload

    def normalize_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class RegisterResponse:
    uid: str
    email: str
    display_name: Optional[str]
    email_verified: bool
    created_at: datetime
    tokens: Optional[Dict[str, str]] = None
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "uid": self.uid,
            "email": self.email,
            "display_name": self.display_name,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat(),
        }
        if self.tokens:
            result["tokens"] = self.tokens
        return result


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_firebase_payload(self) -> Dict[str, Any]:
        return {
            "email": self.email.strip().lower(),
            "password": self.password,
            "returnSecureToken": True,
        }

    def normalize_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class LoginResponse:
    uid: str
    email: str
    display_name: Optional[str]
    id_token: str
    refresh_token: str
    expires_in: int
    is_new_user: bool
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "email": self.email,
            "display_name": self.display_name,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "is_new_user": self.is_new_user,
        }


@dataclass
class RefreshRequest:
    refresh_token: str

    def to_firebase_payload(self) -> Dict[str, Any]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass
class RefreshResponse:
    uid: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uid": self.uid,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
        }


@dataclass
class PasswordResetRequest:
    email: str
    continue_url: Optional[str] = None
    locale: Optional[str] = "en-US"

    def to_firebase_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email.strip().lower(),
            "requestType": "PASSWORD_RESET",
        }
        if self.continue_url:
            payload["continueUrl"] = self.continue_url
        return payload

    def normalize_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class PasswordResetResponse:
    email: str
    oob_code: Optional[str]
    reset_link_sent: bool
    message: str
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "oob_code": self.oob_code,
            "reset_link_sent": self.reset_link_sent,
            "message": self.message,
        }


@dataclass
class FirebaseError:
    code: int
    message: str
    errors: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "errors": self.errors,
        }


def normalize_firebase_error(
    response_data: Dict[str, Any], status_code: int
) -> FirebaseError:
    error_info = response_data.get("error", {})
    return FirebaseError(
        code=error_info.get("code", status_code),
        message=error_info.get("message", "Unknown error"),
        errors=error_info.get("errors", []),
    )


def parse_register_response(
    firebase_data: Dict[str, Any], request: RegisterRequest
) -> RegisterResponse:
    return RegisterResponse(
        uid=firebase_data.get("localId", ""),
        email=firebase_data.get("email", request.email),
        display_name=firebase_data.get("displayName"),
        email_verified=firebase_data.get("emailVerified", False),
        created_at=datetime.now(timezone.utc),
        tokens={
            "id_token": firebase_data.get("idToken", ""),
            "refresh_token": firebase_data.get("refreshToken", ""),
            "expires_in": firebase_data.get("expiresIn", "3600"),
        }
        if "idToken" in firebase_data
        else None,
        raw_response=firebase_data,
    )


def parse_login_response(
    firebase_data: Dict[str, Any], request: LoginRequest
) -> LoginResponse:
    return LoginResponse(
        uid=firebase_data.get("localId", ""),
        email=firebase_data.get("email", request.email),
        display_name=firebase_data.get("displayName"),
        id_token=firebase_data.get("idToken", ""),
        refresh_token=firebase_data.get("refreshToken", ""),
        expires_in=int(firebase_data.get("expiresIn", 3600)),
        is_new_user=firebase_data.get("isNewUser", False),
        raw_response=firebase_data,
    )


def parse_refresh_response(firebase_data: Dict[str, Any]) -> RefreshResponse:
    return RefreshResponse(
        uid=firebase_data.get("user_id", ""),
        id_token=firebase_data.get("id_token", ""),
        refresh_token=firebase_data.get("refresh_token", ""),
        expires_in=int(firebase_data.get("expires_in", 3600)),
        token_type=firebase_data.get("token_type", "Bearer"),
        raw_response=firebase_data,
    )


def parse_password_reset_response(
    firebase_data: Dict[str, Any], request: PasswordResetRequest
) -> PasswordResetResponse:
    return PasswordResetResponse(
        email=request.email,
        oob_code=firebase_data.get("oobCode"),
        reset_link_sent=True,
        message="Password reset email sent successfully",
        raw_response=firebase_data,
    )
