import dataclasses
import typing


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class LoginUserRequest:
    email: str
    password: str
    audience: str
    scope: str = "openid profile email offline_access"
    grant_type: str = "password"


@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str
    client_id: str
    client_secret: str
    audience: str
    scope: str = "openid profile email offline_access"
    grant_type: str = "refresh_token"


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class ProfileNote:
    user_id: str
    timestamp: str
    note: str
    metadata: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
