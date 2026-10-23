from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, MutableMapping, Optional
import base64
import hashlib
import json
import secrets
import urllib.parse


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value).strip() or None


def _first_non_empty(*values: Any) -> Optional[str]:
    for value in values:
        text = _coerce_str(value)
        if text:
            return text
    return None


def _to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on"}:
        return True
    if text in {"false", "0", "no", "n", "off"}:
        return False
    return None


def _to_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _normalize_url(value: Any) -> Optional[str]:
    text = _coerce_str(value)
    if not text:
        return None
    parsed = urllib.parse.urlparse(text)
    if not parsed.scheme or not parsed.netloc:
        return text
    normalized = parsed._replace(fragment="")
    return urllib.parse.urlunparse(normalized)


def _stable_json(data: Mapping[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_b64url(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def generate_state(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_nonce(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_pkce_pair() -> Dict[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = _sha256_b64url(verifier)
    return {"code_verifier": verifier, "code_challenge": challenge, "code_challenge_method": "S256"}


@dataclass(frozen=True)
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    authorization_endpoint: str
    scope: str = "openid profile email"
    response_type: str = "code"
    state: str = field(default_factory=generate_state)
    nonce: Optional[str] = field(default_factory=generate_nonce)
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    prompt: Optional[str] = None
    login_hint: Optional[str] = None
    claims: Optional[Mapping[str, Any]] = None
    additional_params: Mapping[str, Any] = field(default_factory=dict)

    def to_params(self) -> Dict[str, str]:
        params: Dict[str, str] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
            "state": self.state,
        }
        if self.nonce:
            params["nonce"] = self.nonce
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.prompt:
            params["prompt"] = self.prompt
        if self.login_hint:
            params["login_hint"] = self.login_hint
        if self.claims:
            params["claims"] = _stable_json(dict(self.claims))
        for key, value in self.additional_params.items():
            if value is None:
                continue
            params[str(key)] = str(value)
        return params

    def to_url(self) -> str:
        return f"{self.authorization_endpoint}?{urllib.parse.urlencode(self.to_params())}"


@dataclass(frozen=True)
class TokenRequest:
    token_endpoint: str
    client_id: str
    client_secret: Optional[str] = None
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    grant_type: str = "authorization_code"
    code_verifier: Optional[str] = None
    refresh_token: Optional[str] = None
    additional_params: Mapping[str, Any] = field(default_factory=dict)

    def to_form(self) -> Dict[str, str]:
        form: Dict[str, str] = {"grant_type": self.grant_type, "client_id": self.client_id}
        if self.code is not None:
            form["code"] = self.code
        if self.redirect_uri is not None:
            form["redirect_uri"] = self.redirect_uri
        if self.code_verifier is not None:
            form["code_verifier"] = self.code_verifier
        if self.refresh_token is not None:
            form["refresh_token"] = self.refresh_token
        for key, value in self.additional_params.items():
            if value is None:
                continue
            form[str(key)] = str(value)
        return form


@dataclass(frozen=True)
class TokenResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TokenResponse":
        return cls(
            access_token=_coerce_str(data.get("access_token")),
            id_token=_coerce_str(data.get("id_token")),
            refresh_token=_coerce_str(data.get("refresh_token")),
            token_type=_coerce_str(data.get("token_type")),
            expires_in=_to_int(data.get("expires_in")),
            scope=_coerce_str(data.get("scope")),
            raw=dict(data),
        )


@dataclass(frozen=True)
class UserProfileClaims:
    subject: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    issuer: Optional[str] = None
    audience: Optional[str] = None
    expiration_time: Optional[datetime] = None
    issued_at: Optional[datetime] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "UserProfileClaims":
        return cls(
            subject=_first_non_empty(data.get("sub"), data.get("subject")),
            email=_first_non_empty(data.get("email")),
            email_verified=_to_bool(data.get("email_verified")),
            name=_first_non_empty(data.get("name")),
            given_name=_first_non_empty(data.get("given_name")),
            family_name=_first_non_empty(data.get("family_name")),
            preferred_username=_first_non_empty(data.get("preferred_username"), data.get("username"), data.get("login")),
            picture=_normalize_url(data.get("picture")),
            locale=_first_non_empty(data.get("locale")),
            issuer=_normalize_url(data.get("iss")),
            audience=_first_non_empty(data.get("aud")),
            expiration_time=_to_datetime(data.get("exp")),
            issued_at=_to_datetime(data.get("iat")),
            raw=dict(data),
        )

    @property
    def display_name(self) -> Optional[str]:
        return _first_non_empty(self.name, self.preferred_username, self.email, self.subject)


@dataclass(frozen=True)
class AuthorizationCallback:
    code: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    issuer: Optional[str] = None
    raw_query: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_query_params(cls, params: Mapping[str, Any]) -> "AuthorizationCallback":
        return cls(
            code=_coerce_str(params.get("code")),
            state=_coerce_str(params.get("state")),
            error=_coerce_str(params.get("error")),
            error_description=_coerce_str(params.get("error_description")),
            issuer=_normalize_url(params.get("iss")),
            raw_query=dict(params),
        )

    @property
    def is_error(self) -> bool:
        return self.error is not None

    @property
    def is_success(self) -> bool:
        return self.code is not None and self.error is None


def normalize_query_string(query: str) -> Dict[str, str]:
    parsed = urllib.parse.parse_qs(query, keep_blank_values=True)
    return {key: values[-1] for key, values in parsed.items() if values}


def normalize_json_mapping(data: Any) -> Dict[str, Any]:
    if isinstance(data, MutableMapping):
        return dict(data)
    if isinstance(data, Mapping):
        return dict(data)
    if isinstance(data, str):
        loaded = json.loads(data)
        if isinstance(loaded, Mapping):
            return dict(loaded)
    raise TypeError("Expected a mapping or JSON object string")
