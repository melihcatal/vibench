from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_dict(value: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in value.items() if v is not None}


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_cognito_attributes(self) -> List[Dict[str, str]]:
        attrs = []
        if self.display_name:
            attrs.append({"Name": "name", "Value": self.display_name})
        return attrs


@dataclass
class RegisterUserResponse:
    provider: str
    user_sub: Optional[str]
    user_confirmed: bool
    delivery_destination: Optional[str] = None
    delivery_medium: Optional[str] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "user_sub": self.user_sub,
                "user_confirmed": self.user_confirmed,
                "delivery_destination": self.delivery_destination,
                "delivery_medium": self.delivery_medium,
                "message": self.message,
            }
        )


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class TokenSet:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    provider: str = "amazon-cognito-idp"

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "id_token": self.id_token,
                "token_type": self.token_type,
                "expires_in": self.expires_in,
            }
        )


@dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    provider: str
    delivery_destination: Optional[str]
    delivery_medium: Optional[str]
    message: str

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "delivery_destination": self.delivery_destination,
                "delivery_medium": self.delivery_medium,
                "message": self.message,
            }
        )


@dataclass
class TranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class TranslationResponse:
    provider: str
    translated_text: str
    target_locale: str
    detected_source_locale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "provider": self.provider,
                "translated_text": self.translated_text,
                "target_locale": self.target_locale,
                "detected_source_locale": self.detected_source_locale,
            }
        )


@dataclass
class ModerationRequest:
    text: str
    locale: Optional[str] = "en"


@dataclass
class ModerationResponse:
    provider: str
    allowed: bool
    scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "allowed": self.allowed,
            "scores": self.scores,
            "flagged_categories": self.flagged_categories,
        }


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    email: str
    locale: str
    completed_steps: List[str]
    pending_steps: List[str]
    profile_note: Optional[str] = None


@dataclass
class OnboardingSummaryResponse:
    provider: str
    model: str
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "summary": self.summary,
        }


@dataclass
class ProfileNoteStoreRequest:
    user_id: str
    email: str
    locale: str
    notes: List[str]
    support_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_document(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "locale": self.locale,
            "notes": self.notes,
            "support_metadata": self.support_metadata,
            "updated_at": utc_now_iso(),
        }


@dataclass
class ProfileNoteStoreResponse:
    provider: str
    document_id: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "document_id": self.document_id,
            "status": self.status,
        }
