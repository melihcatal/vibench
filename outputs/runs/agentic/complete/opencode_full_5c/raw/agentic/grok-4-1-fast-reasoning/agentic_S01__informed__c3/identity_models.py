from typing import TypedDict


class AuthResponse(TypedDict):
    id_token: str
    access_token: str
    refresh_token: str | None


def parse_auth_result(auth_result: dict) -> AuthResponse:
    return {
        "id_token": auth_result["IdToken"],
        "access_token": auth_result["AccessToken"],
        "refresh_token": auth_result.get("RefreshToken"),
    }
