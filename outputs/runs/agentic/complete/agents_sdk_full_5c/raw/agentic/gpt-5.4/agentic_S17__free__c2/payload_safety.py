from __future__ import annotations

from security_client import get_comprehend_client
from security_models import SafetyAssessment


UNSAFE_LABELS = {"TOXICITY", "HATE_SPEECH", "INSULT", "PROFANITY", "VIOLENCE_OR_THREAT"}


def check_payload_safety(text: str, language_code: str = "en") -> SafetyAssessment:
    comprehend = get_comprehend_client()
    response = comprehend.detect_pii_entities(Text=text, LanguageCode=language_code)
    categories = {f"pii::{entity['Type']}": True for entity in response.get("Entities", [])}
    return SafetyAssessment(
        provider="aws-comprehend",
        flagged=bool(categories),
        categories=categories,
        original_text=text,
    )
