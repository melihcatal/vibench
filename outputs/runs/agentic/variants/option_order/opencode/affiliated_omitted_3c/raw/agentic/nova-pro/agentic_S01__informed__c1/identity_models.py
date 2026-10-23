from typing import Any, Dict


class CreateUserRequest:
    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password


class CreateUserResponse:
    def __init__(self, user_id: str, status: str):
        self.user_id = user_id
        self.status = status
