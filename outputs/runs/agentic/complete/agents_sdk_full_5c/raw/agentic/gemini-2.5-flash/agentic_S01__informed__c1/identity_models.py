"""
Define local request, response, and normalization helpers for Email/Password Account Lifecycle.
"""

from typing import Optional, Dict, Any

class UserRegistrationRequest:
    def __init__(self, email: str, password: str, display_name: Optional[str] = None):
        self.email = email
        self.password = password
        self.display_name = display_name

    def to_dict(self):
        data = {"email": self.email, "password": self.password}
        if self.display_name:
            data["displayName"] = self.display_name
        return data

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self):
        return {"email": self.email, "password": self.password}

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

    def to_dict(self):
        return {"email": self.email}

class UserResponse:
    def __init__(self, uid: str, email: str, display_name: Optional[str] = None, **kwargs):
        self.uid = uid
        self.email = email
        self.display_name = display_name
        self.extra_data = kwargs

    @classmethod
    def from_firebase_user_record(cls, user_record: Any): # firebase_admin.auth.UserRecord
        return cls(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            email_verified=user_record.email_verified,
            phone_number=user_record.phone_number,
            photo_url=user_record.photo_url,
            disabled=user_record.disabled,
            creation_timestamp=user_record.creation_timestamp,
            last_sign_in_timestamp=user_record.last_sign_in_timestamp
        )

    def to_dict(self):
        data = {
            "uid": self.uid,
            "email": self.email,
        }
        if self.display_name:
            data["displayName"] = self.display_name
        data.update(self.extra_data)
        return data
