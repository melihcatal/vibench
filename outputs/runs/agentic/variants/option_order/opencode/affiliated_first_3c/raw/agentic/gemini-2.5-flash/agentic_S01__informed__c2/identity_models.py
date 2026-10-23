import dataclasses


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str


@dataclasses.dataclass
class RegisterUserResponse:
    uid: str
    email: str


@dataclasses.dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclasses.dataclass
class EmailPasswordLoginResponse:
    custom_token: (
        str  # Firebase Admin SDK generates custom tokens for client-side login
    )


@dataclasses.dataclass
class RefreshSessionRequest:
    id_token: str


@dataclasses.dataclass
class RefreshSessionResponse:
    is_valid: bool  # Firebase Admin SDK verifies token, doesn't directly issue new refresh tokens


@dataclasses.dataclass
class PasswordResetRequest:
    email: str


@dataclasses.dataclass
class PasswordResetResponse:
    message: str
