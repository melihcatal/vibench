from dataclasses import dataclass, field
from typing import Optional

@dataclass

class AuthResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass

class UserProfile:
    subject: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass

class AuditEvent:
    user_id: Optional[str] = None
    event_type: str = ""
    details: dict = field(default_factory=dict)
    timestamp: str = ""

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

@dataclass

class TranslatedConsent:
    consent_text: str = ""
    translated_text: Optional[str] = None
    source_lang: str = ""
    target_lang: str = ""

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

@dataclass

class ModeratedClaim:
    original: str = ""
    moderated: Optional[str] = None
    reason: Optional[str] = None

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}
