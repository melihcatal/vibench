# [HELPER] identity_models.py
# Local request, response, and normalization helpers for Email/Password Account Lifecycle
import uuid
from datetime import datetime, timedelta


class RegisterRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self):
        return {"email": self.email, "password": self.password}


class LoginResponse:
    def __init__(self, access_token: str, refresh_token: str, local_jwt: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.local_jwt = local_jwt
        self.expires_at = datetime.utcnow() + timedelta(seconds=3600)  # dummy expiry

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "local_jwt": self.local_jwt,
            "expires_at": self.expires_at.isoformat(),
        }


class ResetRequest:
    def __init__(self, email: str, reset_token: str):
        self.email = email
        self.reset_token = reset_token

    def to_dict(self):
        return {"email": self.email, "reset_token": self.reset_token}


class ProfileUpdate:
    def __init__(self, user_id: str, profile_text: str):
        self.user_id = user_id
        self.profile_text = profile_text

    def to_dict(self):
        return {"user_id": self.user_id, "profile_text": self.profile_text}


class OnboardingSummary:
    def __init__(self, user_id: str, steps_completed: list, notes: dict):
        self.user_id = user_id
        self.steps_completed = steps_completed
        self.notes = notes

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "steps_completed": self.steps_completed,
            "notes": self.notes,
        }
