from typing import Dict


class LoginRequest:
    def __init__(self, ClientId: str, Username: str, Password: str):
        self.ClientId = ClientId
        self.Username = Username
        self.Password = Password

    @staticmethod
    def from_dict(data: Dict):
        return LoginRequest(data['ClientId'], data['Username'], data['Password'])

    def to_dict(self):
        return {'ClientId': self.ClientId, 'Username': self.Username, 'Password': self.Password}


class LoginResponse:
    def __init__(self, AuthenticationResult: Dict):
        self.AuthenticationResult = AuthenticationResult

    @staticmethod
    def from_dict(data: Dict):
        return LoginResponse(data['AuthenticationResult'])

    def to_dict(self):
        return {'AuthenticationResult': self.AuthenticationResult}


class RefreshRequest:
    def __init__(self, ClientId: str, RefreshToken: str):
        self.ClientId = ClientId
        self.RefreshToken = RefreshToken

    @staticmethod
    def from_dict(data: Dict):
        return RefreshRequest(data['ClientId'], data['RefreshToken'])

    def to_dict(self):
        return {'ClientId': self.ClientId, 'RefreshToken': self.RefreshToken}


class RefreshResponse:
    def __init__(self, AuthenticationResult: Dict):
        self.AuthenticationResult = AuthenticationResult

    @staticmethod
    def from_dict(data: Dict):
        return RefreshResponse(data['AuthenticationResult'])

    def to_dict(self):
        return {'AuthenticationResult': self.AuthenticationResult}


class ResetRequest:
    def __init__(self, ClientId: str, Username: str):
        self.ClientId = ClientId
        self.Username = Username

    @staticmethod
    def from_dict(data: Dict):
        return ResetRequest(data['ClientId'], data['Username'])

    def to_dict(self):
        return {'ClientId': self.ClientId, 'Username': self.Username}