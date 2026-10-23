from typing import TypedDict, List, Dict, Any

class UserAttribute(TypedDict):
    Name: str
    Value: str

class AuthenticationResult(TypedDict):
    AccessToken: str
    IdToken: str
    RefreshToken: str
    ExpiresIn: int
    TokenType: str

def build_user_attributes(email: str) -> List[UserAttribute]:
    return [
        {'Name': 'email', 'Value': email},
        {'Name': 'email_verified', 'Value': 'true'}
    ]

def parse_auth_result(result: Dict[str, Any]) -> AuthenticationResult:
    return result['AuthenticationResult']