from typing import Dict


class RegisterUserResponse:
    def __init__(self, user_confirmed: bool, code_delivery_details: Dict):
        self.user_confirmed = user_confirmed
        self.code_delivery_details = code_delivery_details


class EmailPasswordLoginResponse:
    def __init__(self, authentication_result: Dict):
        self.authentication_result = authentication_result


class RefreshSessionResponse:
    def __init__(self, authentication_result: Dict):
        self.authentication_result = authentication_result


class PasswordResetResponse:
    def __init__(self, code_delivery_details: Dict):
        self.code_delivery_details = code_delivery_details
