import os
import re
import json
from typing import Optional

from security_models import SafetyCheckResult
from security_client import create_openai_completion

OPENAI_MODEL = os.environ.get("SAFETY_CHECK_MODEL", "gpt-4o-mini")

UNSAFE_PATTERNS = [
    r"(?i)password",
    r"(?i)secret",
    r"(?i)token",
    r"(?i)private.?key",
    r"(?i)credential",
    r"(?i)api.?key",
    r"(?i)access.?key",
]


def check_label_safety(
    label: str,
    secret_name: str = "",
    model: str = None,
) -> SafetyCheckResult:
    target_model = model or OPENAI_MODEL

    prompt = (
        f"Analyze the following secret label or note for unsafe content. "
        f"Unsafe content includes: embedded passwords, API keys, tokens, "
        f"private keys, credentials, or any sensitive data that should not "
        f"appear in labels or metadata.\n\n"
        f"Label: {label}\n\n"
        f"Respond with JSON only:\n"
        f'{{"is_safe": true/false, "flagged_terms": ["term1", ...], '
        f'"confidence": 0.0-1.0, "explanation": "brief reason"}}'
    )

    messages = [
        {
            "role": "system",
            "content": "You are a security auditor checking secret labels for unsafe content.",
        },
        {"role": "user", "content": prompt},
    ]

    try:
        response_text = create_openai_completion(
            messages=messages,
            model=target_model,
            temperature=0.0,
            max_tokens=256,
        )

        result = json.loads(response_text)
    except Exception:
        flagged = _regex_check(label)
        result = {
            "is_safe": len(flagged) == 0,
            "flagged_terms": flagged,
            "confidence": 0.5,
            "explanation": "Fallback regex analysis; LLM response was unparsable.",
        }

    return SafetyCheckResult(
        secret_name=secret_name,
        label=label,
        is_safe=result.get("is_safe", True),
        flagged_terms=result.get("flagged_terms", []),
        confidence=result.get("confidence", 0.0),
        explanation=result.get("explanation", ""),
    )


def _regex_check(text: str) -> list:
    flagged = []
    for pattern in UNSAFE_PATTERNS:
        matches = re.findall(pattern, text)
        flagged.extend(matches)
    return list(set(flagged))


def batch_check_labels(
    labels: list,
    secret_name: str = "",
    model: str = None,
) -> list:
    results = []
    for label in labels:
        result = check_label_safety(label, secret_name, model)
        results.append(result)
    return results
