from dataclasses import dataclass


@dataclass
class LoginRequest:
    ClientId: str
    Username: str
    Password: str

    @staticmethod
    def to_dict(self):
        return {'ClientId': self.ClientId, 'Username': self.Username, 'Password': self.Password}


@dataclass
class LoginResponse:
    AuthenticationResult: dict

    @staticmethod
    def from_dict(data):
        return LoginResponse(AuthenticationResult=data['AuthenticationResult'])

    def to_dict(self):
        return {'AuthenticationResult': self.AuthenticationResult}


@dataclass
class RefreshRequest:
    ClientId: str
    RefreshToken: str

    @staticmethod
    def to_dict(self):
        return {'ClientId': self.ClientId, 'RefreshToken': self.RefreshToken}


@dataclass
class RefreshResponse:
    AuthenticationResult: dict

    @staticmethod
    def from_dict(data):
        return RefreshResponse(AuthenticationResult=data['AuthenticationResult'])

    def to_dict(self):
        return {'AuthenticationResult': self.AuthenticationResult}