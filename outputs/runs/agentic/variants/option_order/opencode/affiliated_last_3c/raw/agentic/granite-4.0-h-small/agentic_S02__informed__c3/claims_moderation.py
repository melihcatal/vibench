import os
from typing import TypedDict, Literal
from identity_models import ContentModerationResult, ModerationAction

# Example free-text claim to be moderated
CLAIM_FIELD = "notes"


class ClaimModeration(TypedDict):
    field: str
    original: str
    normalized: str
    action: Literal["retain", "redact", "replace"]
    reason: str | None


def claims_moderation(raw: str) -> ClaimModeration:
    """Moderate free-text claims/notes.
    Applies simple profanity filter and returns moderation decision.
    """
    words = set(raw.lower().split())
    profane = {"badword1", "badword2"}  # placeholder list
    if profane.intersection(words):
        return ClaimModeration(
            field=CLAIM_FIELD,
            original=raw,
            normalized=raw,
            action="replace",
            reason="contains profanity",
        )
    return ClaimModeration(
        field=CLAIM_FIELD,
        original=raw,
        normalized=raw.strip(),
        action="retain",
        reason=None,
    )
