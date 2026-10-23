from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _compact_dict(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_supabase_payload(self) -> Dict[str, Any]:
        metadata = _compact_dict({"display_name": self.display_name})
        return _compact_dict(
            {
                "email": self.email,
                "password": self.password,
                "data": metadata or None,
            }
        )


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_supabase_payload(self) -> Dict[str, Any]:
        return {"email": self.email, "password": self.password}


@dataclass
class RefreshSessionRequest:
    refresh_token: str

    def to_supabase_payload(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass
class PasswordResetRequest:
    email: str
    redirect_to: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class ModerationRequest:
    profile_text: str


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    locale: str
    steps_completed: List[str] = field(default_factory=list)
    profile_text: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ProfileNoteStoreRequest:
    user_id: str
    email: str
    locale: str
    notes: str
    support_metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_supabase_auth_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = payload.get("user") or {}
    return {
        "user": {
            "id": user.get("id"),
            "email": user.get("email"),
            "display_name": (user.get("user_metadata") or {}).get("display_name"),
            "created_at": user.get("created_at"),
        },
        "session": normalize_session(payload.get("session") or payload),
    }


def normalize_session(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "access_token": payload.get("access_token"),
        "refresh_token": payload.get("refresh_token"),
        "token_type": payload.get("token_type"),
        "expires_in": payload.get("expires_in"),
        "expires_at": payload.get("expires_at"),
    }


def normalize_translation(payload: Dict[str, Any]) -> Dict[str, Any]:
    translations = payload.get("data", {}).get("translations", [])
    text = translations[0]["translatedText"] if translations else ""
    detected = translations[0].get("detectedSourceLanguage") if translations else None
    return {"translated_text": text, "detected_source_language": detected}


def normalize_openai_moderation(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = (payload.get("results") or [{}])[0]
    return {
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
    }


def normalize_openai_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    output = payload.get("output", [])
    text_parts: List[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(content.get("text", ""))
    return {"summary": "\n".join(part for part in text_parts if part).strip()}


def firestore_document(
    user_id: str, email: str, locale: str, notes: str, support_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    fields: Dict[str, Any] = {
        "user_id": {"stringValue": user_id},
        "email": {"stringValue": email},
        "locale": {"stringValue": locale},
        "notes": {"stringValue": notes},
    }
    metadata_fields = {
        key: {"stringValue": str(value)} for key, value in support_metadata.items()
    }
    fields["support_metadata"] = {"mapValue": {"fields": metadata_fields}}
    return {"fields": fields}
