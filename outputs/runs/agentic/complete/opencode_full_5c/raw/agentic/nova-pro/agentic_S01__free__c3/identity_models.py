from typing import Any, Dict


class User:
    def __init__(self, uid: str, email: str, password: str):
        self.uid = uid
        self.email = email
        self.password = password


class Tokens:
    def __init__(self, id_token: str, refresh_token: str):
        self.id_token = id_token
        self.refresh_token = refresh_token
