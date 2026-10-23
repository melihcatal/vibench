from typing import Dict


class RegisterUserRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, user_id: str):
        self.user_id = user_id


class EmailPasswordLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class EmailPasswordLoginResponse:
    def __init__(self, id_token: str, refresh_token: str):
        self.id_token = id_token
        self.refresh_token = refresh_token


class RefreshSessionRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token


class RefreshSessionResponse:
    def __init__(self, id_token: str):
        self.id_token = id_token


class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email


class PasswordResetResponse:
    def __init__(self, success: bool):
        self.success = success
