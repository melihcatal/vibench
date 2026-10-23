import json
from dataclasses import dataclass

def normalize_email(email):
    return email.strip().lower()

def normalize_password(password):
    return password.strip()

def parse_json_response(body):
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return json.loads(body)

@dataclass
class RegistrationRequest:
    email: str
    password: str
    locale: str = None
    metadata: dict = None
    def to_dict(self):
        data = {'email': self.email, 'password': self.password}
        if self.locale is not None:
            data['locale'] = self.locale
        if self.metadata is not None:
            data['metadata'] = self.metadata
        return data

@dataclass
class RegistrationResponse:
    user_id: str = None
    status: str = None
    @classmethod
    def from_dict(cls, data):
        return cls(user_id=data.get('user_id'), status=data.get('status'))
    def to_dict(self):
        return {'user_id': self.user_id, 'status': self.status}

@dataclass
class LoginRequest:
    email: str
    password: str
    def to_dict(self):
        return {'email': self.email, 'password': self.password}

@dataclass
class LoginResponse:
    access_token: str = None
    refresh_token: str = None
    @classmethod
    def from_dict(cls, data):
        return cls(access_token=data.get('access_token'), refresh_token=data.get('refresh_token'))
    def to_dict(self):
        return {'access_token': self.access_token, 'refresh_token': self.refresh_token}

@dataclass
class RefreshRequest:
    refresh_token: str
    def to_dict(self):
        return {'refresh_token': self.refresh_token}

@dataclass
class RefreshResponse:
    access_token: str = None
    @classmethod
    def from_dict(cls, data):
        return cls(access_token=data.get('access_token'))
    def to_dict(self):
        return {'access_token': self.access_token}

@dataclass
class PasswordResetRequest:
    email: str
    def to_dict(self):
        return {'email': self.email}

@dataclass
class PasswordResetResponse:
    reset_token: str = None
    @classmethod
    def from_dict(cls, data):
        return cls(reset_token=data.get('reset_token'))
    def to_dict(self):
        return {'reset_token': self.reset_token}
