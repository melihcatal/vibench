from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    given_name: str = ""
    family_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": "Username-Password-Authentication",
        }
        if self.given_name:
            payload["given_name"] = self.given_name
        if self.family_name:
            payload["family_name"] = self.family_name
        if self.metadata:
            payload["user_metadata"] = self.metadata
        return payload


@dataclass
class UserRegistrationResponse:
    user_id: str
    email: str
    email_verified: bool = False
    created_at: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "UserRegistrationResponse":
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=data.get("created_at"),
            raw_response=data,
        )


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: str = ""
    scope: str = "openid profile email"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "client_id": client_id,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int = 86400
    refresh_token: Optional[str] = None
    scope: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            refresh_token=data.get("refresh_token"),
            scope=data.get("scope", ""),
            raw_response=data,
        )


@dataclass
class RefreshRequest:
    refresh_token: str
    audience: str = ""

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": self.refresh_token,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class RefreshResponse:
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int = 86400
    scope: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RefreshResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            scope=data.get("scope", ""),
            raw_response=data,
        )


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class PasswordResetResponse:
    email: str
    connection: str
    ticket_id: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=data.get("email", ""),
            connection=data.get("connection", ""),
            ticket_id=data.get("ticket_id"),
            raw_response=data,
        )


@dataclass
class TranslationRequest:
    text: str
    target_lang: str
    source_lang: Optional[str] = None

    def to_deepl_params(self) -> Dict[str, Any]:
        params = {
            "text": self.text,
            "target_lang": self.target_lang.upper(),
        }
        if self.source_lang:
            params["source_lang"] = self.source_lang.upper()
        return params


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_lang: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_deepl_result(cls, result: Dict[str, Any]) -> "TranslationResponse":
        return cls(
            translated_text=result.get("text", ""),
            detected_source_lang=result.get("detected_source_lang"),
            raw_response=result,
        )


@dataclass
class ModerationRequest:
    text: str
    attributes: List[str] = field(
        default_factory=lambda: [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "PROFANITY",
        ]
    )

    def to_perspective_payload(self, api_key: str) -> Dict[str, Any]:
        return {
            "comment": {"text": self.text},
            "requestedAttributes": {attr: {} for attr in self.attributes},
            "clientToken": api_key,
        }


@dataclass
class ModerationResult:
    attribute: str
    score: float
    flagged: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attribute": self.attribute,
            "score": self.score,
            "flagged": self.flagged,
        }


@dataclass
class ModerationResponse:
    results: List[ModerationResult] = field(default_factory=list)
    overall_flagged: bool = False
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_perspective_response(
        cls, data: Dict[str, Any], threshold: float = 0.7
    ) -> "ModerationResponse":
        results = []
        overall_flagged = False
        attribute_scores = data.get("attributeScores", {})
        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            flagged = score >= threshold
            if flagged:
                overall_flagged = True
            results.append(
                ModerationResult(
                    attribute=attr_name,
                    score=score,
                    flagged=flagged,
                )
            )
        return cls(
            results=results,
            overall_flagged=overall_flagged,
            raw_response=data,
        )


@dataclass
class SummaryRequest:
    onboarding_data: Dict[str, Any]
    model: str = "claude-sonnet-4-20250514"

    def to_anthropic_messages(self) -> List[Dict[str, str]]:
        data_str = _format_onboarding_data(self.onboarding_data)
        return [
            {
                "role": "user",
                "content": (
                    f"Summarize the following user onboarding state for a support agent. "
                    f"Include account status, locale, moderation results, and any flags.\n\n"
                    f"{data_str}"
                ),
            }
        ]


def _format_onboarding_data(data: Dict[str, Any]) -> str:
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        elif isinstance(value, list):
            lines.append(f"{key}: {', '.join(str(v) for v in value)}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


@dataclass
class SummaryResponse:
    summary_text: str
    model: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_anthropic_response(cls, data: Dict[str, Any]) -> "SummaryResponse":
        content_blocks = data.get("content", [])
        summary = ""
        for block in content_blocks:
            if block.get("type") == "text":
                summary = block.get("text", "")
                break
        return cls(
            summary_text=summary,
            model=data.get("model", ""),
            raw_response=data,
        )


@dataclass
class NoteStoreRequest:
    user_id: str
    notes: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_mongo_document(self, collection: str = "onboarding_notes") -> Dict[str, Any]:
        doc = {
            "user_id": self.user_id,
            "notes": self.notes,
            "metadata": self.metadata,
            "collection": collection,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        return doc


@dataclass
class NoteStoreResponse:
    document_id: str
    user_id: str
    acknowledged: bool = True
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mongo_insert(cls, insert_result: Any) -> "NoteStoreResponse":
        return cls(
            document_id=str(insert_result.inserted_id),
            user_id="",
            acknowledged=insert_result.acknowledged,
            raw_response={"inserted_id": str(insert_result.inserted_id)},
        )
