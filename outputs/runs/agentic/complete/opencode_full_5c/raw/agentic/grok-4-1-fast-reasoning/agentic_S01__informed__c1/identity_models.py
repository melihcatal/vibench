from typing import Dict, Any, List


def build_user_attributes(email: str) -> List[Dict[str, str]]:
    return [
        {"Name": "email", "Value": email},
        {"Name": "email_verified", "Value": "true"},
    ]


def parse_register_response(resp: Dict[str, Any]) -> Dict[str, str]:
    return {
        "user_id": resp["User"]["Username"],
        "user_status": resp["User"]["UserStatus"],
    }


def parse_auth_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    auth_result = resp["AuthenticationResult"]
    return {
        "access_token": auth_result.get("AccessToken"),
        "id_token": auth_result.get("IdToken"),
        "refresh_token": auth_result.get("RefreshToken"),
        "expires_in": auth_result.get("ExpiresIn"),
        "token_type": auth_result.get("TokenType"),
    }


def build_admin_auth_params(email: str, password: str) -> Dict[str, str]:
    return {"USERNAME": email, "PASSWORD": password}


def build_refresh_params(refresh_token: str) -> Dict[str, str]:
    return {"REFRESH_TOKEN": refresh_token}
