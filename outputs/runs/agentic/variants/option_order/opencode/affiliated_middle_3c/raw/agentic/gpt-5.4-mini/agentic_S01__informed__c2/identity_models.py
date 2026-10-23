from dataclasses import dataclass


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    name: str = None

    def to_dict(self):
        data = {"email": self.email, "password": self.password, "verify_email": False}
        if self.name:
            data["name"] = self.name
        return data


@dataclass
class RegisterUserResponse:
    data: dict

    @classmethod
    def from_dict(cls, data):
        return cls(data=data)

    def to_dict(self):
        return self.data


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_dict(self):
        return {"username": self.email, "password": self.password}


@dataclass
class RefreshRequest:
    refresh_token: str

    def to_dict(self):
        return {"refresh_token": self.refresh_token}


@dataclass
class PasswordResetRequest:
    email: str
    connection: str

    def to_dict(self):
        return {"email": self.email, "connection": self.connection}


@dataclass
class TokenResponse:
    data: dict

    @classmethod
    def from_dict(cls, data):
        return cls(data=data)

    def to_dict(self):
        return self.data
