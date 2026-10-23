from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional

from safety_client import AzureContentSafetyClient
from safety_models import normalize_analysis_result


def redact_unsafe(
    text: str,
    categories: Optional[Iterable[str]] = None,
    blocklist_names: Optional[Iterable[str]] = None,
    mask: str = "[REDACTED]",
) -> Dict[str, object]:
    client = AzureContentSafetyClient()
    response_json = client.analyze_text(
        text=text,
        categories=categories,
        blocklist_names=blocklist_names,
    )
    result = normalize_analysis_result(text, response_json)
    severe = [c.category for c in result.categories if (c.severity or 0) >= 4]
    redacted_text = text
    spans: List[Dict[str, object]] = []
    if severe:
        for category in severe:
            pattern = re.compile(r"\b\w+\b", re.IGNORECASE)
            for match in pattern.finditer(text):
                token = match.group(0)
                if len(token) > 4:
                    redacted_text = redacted_text.replace(token, mask, 1)
                    spans.append({"category": category, "start": match.start(), "end": match.end()})
                    break
    return {
        "provider": "azure-ai-content-safety",
        "flagged": result.flagged,
        "redacted_text": redacted_text,
        "unsafe_categories": severe,
        "redacted_spans": spans,
        "raw_response": response_json,
    }
