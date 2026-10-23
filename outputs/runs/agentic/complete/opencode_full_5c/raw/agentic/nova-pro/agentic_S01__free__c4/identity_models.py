from typing import Dict


class RegisterUserRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class RegisterUserResponse:
    def __init__(self, data: Dict):
        self.data = data
