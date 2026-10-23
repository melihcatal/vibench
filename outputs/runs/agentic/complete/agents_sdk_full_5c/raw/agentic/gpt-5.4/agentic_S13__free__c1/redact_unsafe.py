from __future__ import annotations

import re
from typing import Dict

from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import DEFAULT_OUTPUT_TYPE, build_thresholds, get_content_safety_client
from safety_models import SafetyDecision, normalize_category_scores, severity_map


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> SafetyDecision:
    client = get_content_safety_client()
    response = client.analyze_text(AnalyzeTextOptions(text=text, output_type=DEFAULT_OUTPUT_TYPE))
    categories = normalize_category_scores([item.as_dict() for item in response.categories_analysis])
    severities = severity_map(categories)
    thresholds = build_thresholds()
    triggered = [name for name, value in severities.items() if value >= thresholds.get(name, 99)]

    redacted_text = text
    if triggered:
        patterns: Dict[str, str] = {
            "self_harm": r"\b(kill myself|suicide|self-harm|cut myself)\b",
            "violence": r"\b(shoot|stab|bomb|murder|kill)\b",
            "hate": r"\b(slur|vermin|subhuman)\b",
            "sexual": r"\b(explicit|nude|sexual act)\b",
        }
        for category in triggered:
            pattern = patterns.get(category)
            if pattern:
                redacted_text = re.sub(pattern, replacement, redacted_text, flags=re.IGNORECASE)
        if redacted_text == text:
            redacted_text = replacement

    return SafetyDecision(
        text=text,
        allowed=not triggered,
        categories=categories,
        redacted_text=redacted_text,
        block_reasons=triggered,
        metadata={"service": "Azure AI Content Safety"},
    )
