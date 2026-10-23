import re
from typing import Optional

from safety_models import (
    ModerationRequest,
    ModerationResponse,
    RedactionResult,
    ModerationDecision,
    SafetyCategory,
    response_to_dict,
)
from safety_client import moderate_single


REDACTION_MARKER = "[REDACTED]"


def _find_unsafe_spans(text: str, response: ModerationResponse) -> list[dict]:
    spans = []
    if response.decision == ModerationDecision.ALLOW:
        return spans

    flagged_cats = response.flagged_categories
    sentences = re.split(r"(?<=[.!?])\s+", text)
    current_pos = 0
    for sentence in sentences:
        stripped = sentence.strip()
        if not stripped:
            current_pos += len(sentence)
            continue

        sentence_request = ModerationRequest(
            text=stripped,
            categories=[c for c in flagged_cats],
        )
        try:
            sentence_response = moderate_single(sentence_request)
        except Exception:
            current_pos += len(sentence)
            continue

        if sentence_response.decision != ModerationDecision.ALLOW:
            spans.append(
                {
                    "start": current_pos,
                    "end": current_pos + len(stripped),
                    "text": stripped,
                    "flagged_categories": [
                        c.value for c in sentence_response.flagged_categories
                    ],
                    "max_score": max(
                        (cs.score for cs in sentence_response.category_scores),
                        default=0.0,
                    ),
                }
            )
        current_pos += len(sentence)

    return spans


def redact_unsafe(
    text: str,
    user_id: Optional[str] = None,
    replacement: str = REDACTION_MARKER,
) -> dict:
    request = ModerationRequest(text=text, user_id=user_id)
    response = moderate_single(request)

    if response.decision == ModerationDecision.ALLOW:
        return {
            "original_text": text,
            "redacted_text": text,
            "flagged_spans": [],
            "decision": response.decision.value,
        }

    flagged_spans = _find_unsafe_spans(text, response)

    redacted = text
    for span in sorted(flagged_spans, key=lambda s: s["start"], reverse=True):
        redacted = redacted[: span["start"]] + replacement + redacted[span["end"] :]

    result = RedactionResult(
        original_text=text,
        redacted_text=redacted,
        flagged_spans=flagged_spans,
        decision=response.decision,
    )

    return {
        "original_text": result.original_text,
        "redacted_text": result.redacted_text,
        "flagged_spans": result.flagged_spans,
        "decision": result.decision.value,
        "category_scores": [
            {"category": cs.category.value, "score": cs.score, "severity": cs.severity}
            for cs in response.category_scores
        ],
    }


def flag_unsafe_only(text: str, user_id: Optional[str] = None) -> dict:
    request = ModerationRequest(text=text, user_id=user_id)
    response = moderate_single(request)

    if response.decision == ModerationDecision.ALLOW:
        return {
            "text": text,
            "is_unsafe": False,
            "flagged_categories": [],
            "decision": response.decision.value,
        }

    return {
        "text": text,
        "is_unsafe": True,
        "flagged_categories": [c.value for c in response.flagged_categories],
        "decision": response.decision.value,
        "category_scores": [
            {"category": cs.category.value, "score": cs.score, "severity": cs.severity}
            for cs in response.category_scores
        ],
    }
