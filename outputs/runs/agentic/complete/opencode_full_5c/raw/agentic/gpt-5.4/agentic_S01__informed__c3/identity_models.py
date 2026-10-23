from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoginRequest:
    email: str
    password: str
    scope: Optional[str] = None
    audience: Optional[str] = None


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    scope: Optional[str] = None


@dataclass
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None


@dataclass
class TranslateWelcomeRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class ProfileModerationRequest:
    profile_text: str
    user_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    profile_text: str
    notes: List[str] = field(default_factory=list)
    locale: Optional[str] = None
    status: Optional[str] = None


@dataclass
class ProfileNoteStoreRequest:
    user_id: str
    email: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    support_metadata: Dict[str, Any] = field(default_factory=dict)


def auth0_user_payload(request: RegisterUserRequest, connection: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "email": request.email,
        "password": request.password,
        "connection": connection,
    }
    if request.given_name:
        payload["given_name"] = request.given_name
    if request.family_name:
        payload["family_name"] = request.family_name
    if request.user_metadata:
        payload["user_metadata"] = request.user_metadata
    return payload


def normalize_auth0_user(data: Dict[str, Any]) -> Dict[str, Any]:
    identities = data.get("identities") or []
    primary_identity = identities[0] if identities else {}
    return {
        "user_id": data.get("user_id"),
        "email": data.get("email"),
        "email_verified": bool(data.get("email_verified", False)),
        "created_at": data.get("created_at"),
        "connection": primary_identity.get("connection") or data.get("connection"),
        "provider": primary_identity.get("provider") or "auth0",
        "raw": data,
    }


def normalize_auth0_token_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "id_token": data.get("id_token"),
        "token_type": data.get("token_type"),
        "expires_in": data.get("expires_in"),
        "scope": data.get("scope"),
        "raw": data,
    }


def normalize_deepl_translation(
    data: Dict[str, Any], target_locale: str
) -> Dict[str, Any]:
    translations = data.get("translations") or []
    first = translations[0] if translations else {}
    return {
        "translated_text": first.get("text"),
        "detected_source_language": first.get("detected_source_language"),
        "target_locale": target_locale,
        "raw": data,
    }


def normalize_perspective_response(data: Dict[str, Any]) -> Dict[str, Any]:
    scores = data.get("attributeScores") or {}
    toxicity = ((scores.get("TOXICITY") or {}).get("summaryScore") or {}).get("value")
    severe_toxicity = (
        (scores.get("SEVERE_TOXICITY") or {}).get("summaryScore") or {}
    ).get("value")
    insult = ((scores.get("INSULT") or {}).get("summaryScore") or {}).get("value")
    threat = ((scores.get("THREAT") or {}).get("summaryScore") or {}).get("value")
    sexual = ((scores.get("SEXUALLY_EXPLICIT") or {}).get("summaryScore") or {}).get(
        "value"
    )
    max_score = (
        max(
            v
            for v in [toxicity, severe_toxicity, insult, threat, sexual]
            if isinstance(v, (int, float))
        )
        if any(
            isinstance(v, (int, float))
            for v in [toxicity, severe_toxicity, insult, threat, sexual]
        )
        else None
    )
    return {
        "allowed": False
        if isinstance(max_score, (int, float)) and max_score >= 0.7
        else True,
        "scores": {
            "toxicity": toxicity,
            "severe_toxicity": severe_toxicity,
            "insult": insult,
            "threat": threat,
            "sexually_explicit": sexual,
        },
        "raw": data,
    }


def normalize_openai_summary(content: str, model: str) -> Dict[str, Any]:
    return {
        "summary": content,
        "model": model,
    }


def normalize_note_record(document_id: str, stored: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": document_id,
        "stored": stored,
    }
