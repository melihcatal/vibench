from typing import Dict


class RegisterUserResponse:
    def __init__(self, user_confirmed: bool, code_delivery_details: Dict):
        self.user_confirmed = user_confirmed
        self.code_delivery_details = code_delivery_details


class LoginResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token


class RefreshSessionResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token


class PasswordResetResponse:
    def __init__(self, code_delivery_details: Dict):
        self.code_delivery_details = code_delivery_details
