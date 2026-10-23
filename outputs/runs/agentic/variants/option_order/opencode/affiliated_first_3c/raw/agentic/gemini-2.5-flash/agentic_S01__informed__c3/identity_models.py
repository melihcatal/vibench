from dataclasses import dataclass


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: str = None


@dataclass
class UserLoginRequest:
    email: str
    password: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class UserResponse:
    uid: str
    email: str
    display_name: str = None
    email_verified: bool = False
    disabled: bool = False
