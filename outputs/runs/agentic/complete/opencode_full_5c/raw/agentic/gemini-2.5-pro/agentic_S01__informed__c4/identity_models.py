from dataclasses import dataclass
from typing import Optional


@dataclass
class UserCredentials:
    email: str
    password: str


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str
    id_token: str


@dataclass
class User:
    user_id: str
    email: str
