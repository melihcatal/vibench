from typing import Dict, List, Optional
from safety_client import TextModerator
from safety_models import normalize_response


def redact_unsafe(text: str, categories: Optional[List[str]] = None) -> Dict:
    """
    Flags or redacts unsafe spans from text using Azure Content Safety.
    Model: 2024-02-15-preview
    """
    moderator = TextModerator()
    response = moderator.moderate_text(text, categories)
    normalized = normalize_response(response)

    if normalized.error:
        return {"redacted_text": text, "unsafe_spans": [], "error": normalized.error}

    unsafe_spans = []
    for analysis in normalized.categories_analysis:
        if analysis.severity > 0:
            unsafe_spans.append(
                {
                    "category": analysis.category,
                    "severity": analysis.severity,
                    "span": {"start": 0, "end": len(text)},
                }
            )

    redacted_text = text
    for span in unsafe_spans:
        redacted_text = redacted_text.replace(
            text[span["span"]["start"] : span["span"]["end"]], "[REDACTED]"
        )

    return {"redacted_text": redacted_text, "unsafe_spans": unsafe_spans, "error": None}
