from typing import Dict


class UserRegistrationRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class UserRegistrationResponse:
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email


class Tokens:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token


class PasswordResetTicket:
    def __init__(self, ticket: str):
        self.ticket = ticket
