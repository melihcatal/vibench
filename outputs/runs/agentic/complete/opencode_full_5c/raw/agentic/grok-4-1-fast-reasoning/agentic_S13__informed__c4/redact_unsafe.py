import os
from typing import Dict, List, Any
from safety_client import post_to_api
from safety_models import SafetyResult


def redact_unsafe(text: str) -> SafetyResult:
    api_key = os.getenv("TISANE_API_KEY")
    url = "https://api.tisane.ai/v1/hate-speech/obfuscate"
    payload = {"content": text, "language": "en"}
    data = post_to_api(url, payload, api_key)
    obfuscated = data.get("obfuscated_content", text)
    violations = data.get("violations", [])
    flagged_spans: List[Dict[str, Any]] = []
    categories: Dict[str, float] = {}
    for v in violations:
        index = v.get("index", 0)
        replacement = v.get("replacement", "[REDACTED]")
        span = {
            "start": index,
            "end": index + len(replacement),
            "replacement": replacement,
            "category": v.get("label", "unknown"),
        }
        flagged_spans.append(span)
        cat = v.get("label", "unknown").lower()
        categories[cat] = 1.0
    overall_blocked = bool(violations)
    rationale = (
        f"Tisane detected and redacted {len(violations)} violations"
        if violations
        else "Clean content"
    )
    return {
        "categories": categories,
        "overall_blocked": overall_blocked,
        "rationale": rationale,
        "redacted_text": obfuscated,
        "flagged_spans": flagged_spans,
        "raw_response": data,
    }
