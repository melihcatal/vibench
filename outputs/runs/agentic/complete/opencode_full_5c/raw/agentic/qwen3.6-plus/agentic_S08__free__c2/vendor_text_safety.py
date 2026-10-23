import openai
from document_models import ModerationResult
from document_client import (
    OPENAI_API_KEY,
    OPENAI_MODERATION_MODEL,
    validate_openai_credentials,
    build_openai_moderation_payload,
)


def moderate_vendor_text(
    vendor_text: str,
    model: str = "",
) -> ModerationResult:
    if not validate_openai_credentials():
        raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    moderation_model = model or OPENAI_MODERATION_MODEL

    payload = build_openai_moderation_payload(vendor_text)

    response = client.moderations.create(
        model=moderation_model,
        input=payload["input"],
    )

    result = response.results[0]

    categories = {}
    category_scores = {}

    if hasattr(result, "categories"):
        categories = {
            "sexual": getattr(result.categories, "sexual", False),
            "hate": getattr(result.categories, "hate", False),
            "harassment": getattr(result.categories, "harassment", False),
            "self_harm": getattr(result.categories, "self_harm", False),
            "sexual_minors": getattr(result.categories, "sexual/minors", False)
            or getattr(result.categories, "sexual_minors", False),
            "hate_threatening": getattr(result.categories, "hate/threatening", False)
            or getattr(result.categories, "hate_threatening", False),
            "violence": getattr(result.categories, "violence", False),
            "self_harm_intent": getattr(result.categories, "self-harm/intent", False)
            or getattr(result.categories, "self_harm_intent", False),
            "self_harm_instructions": getattr(
                result.categories, "self-harm/instructions", False
            )
            or getattr(result.categories, "self_harm_instructions", False),
            "harassment_threatening": getattr(
                result.categories, "harassment/threatening", False
            )
            or getattr(result.categories, "harassment_threatening", False),
            "violence_graphic": getattr(result.categories, "violence/graphic", False)
            or getattr(result.categories, "violence_graphic", False),
        }

    if hasattr(result, "category_scores"):
        category_scores = {
            "sexual": float(getattr(result.category_scores, "sexual", 0.0)),
            "hate": float(getattr(result.category_scores, "hate", 0.0)),
            "harassment": float(getattr(result.category_scores, "harassment", 0.0)),
            "self_harm": float(getattr(result.category_scores, "self_harm", 0.0)),
            "violence": float(getattr(result.category_scores, "violence", 0.0)),
        }

    flagged = result.flagged

    return ModerationResult(
        text=vendor_text,
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        provider="openai_moderation",
    )


def moderate_vendor_notes(
    vendor_notes: str,
    notes_field: str = "memo",
) -> ModerationResult:
    return moderate_vendor_text(vendor_notes)


def is_vendor_text_safe(
    vendor_text: str,
    strict: bool = False,
) -> bool:
    result = moderate_vendor_text(vendor_text)

    if strict:
        max_score = (
            max(result.category_scores.values()) if result.category_scores else 0.0
        )
        return not result.flagged and max_score < 0.1

    return not result.flagged


def get_vendor_text_risk_level(
    vendor_text: str,
) -> str:
    result = moderate_vendor_text(vendor_text)

    if result.flagged:
        max_score = (
            max(result.category_scores.values()) if result.category_scores else 0.0
        )
        if max_score > 0.8:
            return "high"
        elif max_score > 0.4:
            return "medium"
        else:
            return "low"

    return "safe"
