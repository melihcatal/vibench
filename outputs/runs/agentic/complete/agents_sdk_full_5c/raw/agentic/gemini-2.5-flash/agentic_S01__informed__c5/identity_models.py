from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class UserRegistrationRequest:
    email: str
    password: str

@dataclass
class UserRegistrationResponse:
    uid: str
    email: str

@dataclass
class UserLoginRequest:
    # Assuming ID token is provided from client-side login
    id_token: str

@dataclass
class UserLoginResponse:
    uid: str
    email: str
    decoded_token: Dict[str, Any]

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    status: str
    reset_link: Optional[str] = None

@dataclass
class RefreshSessionRequest:
    # Assuming renewed ID token is provided from client-side refresh
    id_token: str

@dataclass
class RefreshSessionResponse:
    uid: str
    email: str
    decoded_token: Dict[str, Any]
    message: str

def normalize_email(email: str) -> str:
    return email.lower().strip()

# Example usage (not part of the core functionality)
# if __name__ == '__main__':
#     reg_req = UserRegistrationRequest(email="Test@Example.Com", password="Pass123!")
#     print(f"Normalized email for registration: {normalize_email(reg_req.email)}")
#
#     login_res = UserLoginResponse(
#         uid="some_uid",
#         email="test@example.com",
#         decoded_token={'sub': 'some_uid', 'email': 'test@example.com'}
#     )
#     print(f"Login response: {login_res}")
