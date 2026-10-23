"""
[SAME-SCENARIO] redact_unsafe.py
Flags or redacts unsafe spans from text using OpenAI Moderation API
for detection, then applies span-level redaction.
Provider: OpenAI — model identifier: text-moderation-latest
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any, List
import re

from safety_client import get_openai_client, load_safety_config
from safety_models import (
    ModerationResult,
    RedactedText,
    normalize_openai_moderation_response,
    CategoryScore,
    ModerationDecision,
)

DEFAULT_MODEL = "text-moderation-latest"
DEFAULT_REDACTION_TOKEN = "[REDACTED]"


def _detect_flagged_keywords(text: str, categories: List[CategoryScore], threshold: float = 0.5) -> List[str]:
    """
    Heuristic: return category names whose scores exceed the threshold.
    These guide span-level redaction by matching known keyword patterns.
    """
    flagged_cats = []
    for cat in categories:
        if cat.score >= threshold:
            flagged_cats.append(cat.category)
    return flagged_cats


def _build_redaction_patterns(flagged_categories: List[str]) -> List[re.Pattern]:
    """
    Build simple regex patterns for common unsafe terms mapped to flagged categories.
    This is a heuristic complement to the API-level moderation scores.
    """
    category_keywords = {
        "sexual": r"\b(sex|nude|porn|explicit|naked)\b",
        "violence": r"\b(kill|murder|blood|weapon|gun|bomb|shoot|stab|attack)\b",
        "hate": r"\b(hate|slur|racist|bigot)\b",
        "hate_threatening": r"\b(hate|threat|exterminate)\b",
        "self_harm": r"\b(suicide|self.?harm|cut.?myself|end.?it.?all)\b",
        "harassment": r"\b(stalk|harass|bully|threaten)\b",
        "violence_graphic": r"\b(gore|torture|mutilate|dismember)\b",
        "self_harm_instructions": r"\b(how.?to.?suicide|suicide.?method|how.?to.?die)\b",
        "self_harm_intent": r"\b(i.?want.?to.?die|i.?will.?kill.?myself)\b",
        "sexual_minors": r"\b(under.?age|minor|child.*sex)\b",
    }
    patterns = []
    for cat in flagged_categories:
        cat_lower = cat.lower()
        if cat_lower in category_keywords:
            patterns.append(re.compile(category_keywords[cat_lower], re.IGNORECASE))
    return patterns


def _redact_spans_in_text(text: str, patterns: List[re.Pattern], replacement: str = DEFAULT_REDACTION_TOKEN) -> tuple[str, List[Dict[str, Any]], List[str]]:
    """
    Apply regex patterns to find and redact unsafe spans.
    Returns (redacted_text, list_of_flagged_spans, categories_redacted).
    """
    flagged_spans = []
    categories_redacted = set()
    redacted = text

    for pattern in patterns:
        for match in pattern.finditer(redacted):
            # Re-find against original text since replacements shift offsets
            orig_match = pattern.search(text)
            if orig_match:
                start = orig_match.start()
                end = orig_match.end()
                flagged_spans.append({
                    "start": start,
                    "end": end,
                    "matched_text": text[start:end],
                    "pattern": pattern.pattern,
                    "replacement": replacement,
                })
                # Extract category name from pattern
                cat_name = pattern.pattern
                for cat_key, kw_pattern in {
                    "sexual": r"\b(sex|nude|porn|explicit|naked)\b",
                    "violence": r"\b(kill|murder|blood|weapon|gun|bomb|shoot|stab|attack)\b",
                    "hate": r"\b(hate|slur|racist|bigot)\b",
                    "hate_threatening": r"\b(hate|threat|exterminate)\b",
                    "self_harm": r"\b(suicide|self.?harm|cut.?myself|end.?it.?all)\b",
                    "harassment": r"\b(stalk|harass|bully|threaten)\b",
                    "violence_graphic": r"\b(gore|torture|mutilate|dismember)\b",
                    "self_harm_instructions": r"\b(how.?to.?suicide|suicide.?method|how.?to.?die)\b",
                    "self_harm_intent": r"\b(i.?want.?to.?die|i.?will.?kill.?myself)\b",
                    "sexual_minors": r"\b(under.?age|minor|child.*sex)\b",
                }.items():
                    if kw_pattern == cat_name:
                        categories_redacted.add(cat_key)
                        break
        redacted = pattern.sub(replacement, redacted)

    return redacted, flagged_spans, list(categories_redacted)


def redact_unsafe(
    text: str,
    model: str = DEFAULT_MODEL,
    threshold: float = 0.5,
    replacement: str = DEFAULT_REDACTION_TOKEN,
    config: Optional[Dict[str, Any]] = None,
) -> RedactedText:
    """
    Flag and redact unsafe spans from text.
    First uses OpenAI Moderation API to determine which categories are unsafe,
    then applies pattern-based span redaction for flagged categories.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)
    response = client.moderations.create(
        input=text,
        model=model,
    )

    mod_result = normalize_openai_moderation_response(text, response)

    flagged_categories = _detect_flagged_keywords(text, mod_result.categories, threshold=threshold)
    patterns = _build_redaction_patterns(flagged_categories)
    redacted_text, flagged_spans, categories_redacted = _redact_spans_in_text(text, patterns, replacement=replacement)

    return RedactedText(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        categories_redacted=categories_redacted,
    )


def redact_unsafe_dict(
    text: str,
    model: str = DEFAULT_MODEL,
    threshold: float = 0.5,
    replacement: str = DEFAULT_REDACTION_TOKEN,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Redact unsafe spans and return as a dict."""
    result = redact_unsafe(text, model=model, threshold=threshold, replacement=replacement, config=config)
    return result.to_dict()


if __name__ == "__main__":
    sample = "This message contains kill and hate terms."
    result = redact_unsafe_dict(sample)
    print(result)
