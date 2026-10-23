import dataclasses


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class RegisterUserResponse:
    id: str
    email: str
    email_verified: bool


@dataclasses.dataclass
class LoginUserRequest:
    email: str
    password: str
    realm: str = "Username-Password-Authentication"
    scope: str = "openid profile email offline_access"
    audience: str = ""  # Set if needed for specific APIs


@dataclasses.dataclass
class LoginUserResponse:
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str
    token_type: str


@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"


@dataclasses.dataclass
class RefreshTokenResponse:
    access_token: str
    expires_in: int
    id_token: str
    token_type: str


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"
