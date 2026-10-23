from typing import TypedDict, List


class Attribute(TypedDict):
    Name: str
    Value: str


class SignUpResult(TypedDict):
    UserSub: str
    UserAttributes: List[Attribute]
    CodeDeliveryDetails: dict


class AdminAuthResult(TypedDict):
    AuthenticationResult: dict
    User: dict


class Tokens(TypedDict):
    IdToken: str
    AccessToken: str
    RefreshToken: str


class AWSAuthResponse(TypedDict):
    Credentials: dict
    IdentityId: str


# Normalized password reset payload
class ResetPasswordPayload(TypedDict):
    Email: str
    Code: str
    NewPassword: str
    ClientId: str


# Normalized refresh payload
class RefreshPayload(TypedDict):
    IdToken: str  # or refresh token if your flow uses it


d
