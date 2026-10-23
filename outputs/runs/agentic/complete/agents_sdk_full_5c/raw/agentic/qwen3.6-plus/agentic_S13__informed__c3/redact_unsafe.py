"""
Flag or redact unsafe spans from text using Azure AI Content Safety
combined with a local span-redaction strategy.

Provider: Azure AI Content Safety
Endpoint: {azure_endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview
"""

from typing import Dict, List, Optional

from moderate_text import moderate_text
from safety_models import (
    RedactionResult,
    ModerationResponse,
    build_redaction_spans,
)


def _default_replacement(span: Dict) -> str:
    """Default replacement label for a flagged category."""
    return span.get("label", "[UNSAFE]")


def redact_unsafe(
    text: str,
    config: Optional[Dict[str, str]] = None,
    replacement_fn=None,
    redact_full: bool = False,
) -> RedactionResult:
    """
    Analyse *text* via Azure AI Content Safety and either:
      - When redact_full=False, annotate the text with span-level category labels.
      - When redact_full=True, replace the entire text with a single redaction marker.

    Provider: Azure AI Content Safety
    """
    repl_fn = replacement_fn or _default_replacement

    moderation: ModerationResponse = moderate_text(text, config=config)
    flagged_spans = build_redaction_spans(moderation)

    if not flagged_spans or moderation.is_safe:
        return RedactionResult(original=text, redacted=text, flagged_spans=[])

    if redact_full:
        labels = ", ".join(s["category"] for s in flagged_spans)
        redacted = repl_fn({"label": f"[REDACTED: {labels}]"})
        return RedactionResult(
            original=text, redacted=redacted, flagged_spans=flagged_spans
        )

    # Annotate the full text with category labels at the end
    markers = []
    for s in flagged_spans:
        markers.append(f"⚠️ {s['category']} (severity {s['severity']})")
    redacted = text + " | " + " ".join(markers)

    return RedactionResult(
        original=text, redacted=redacted, flagged_spans=flagged_spans
    )


if __name__ == "__main__":
    sample = "Some problematic content about violence."
    result = redact_unsafe(sample)
    print(f"Original: {result.original}")
    print(f"Redacted: {result.redacted}")
    print(f"Spans: {result.flagged_spans}")
