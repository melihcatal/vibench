import os
import hashlib
from typing import Optional, List, Dict
from datetime import datetime

import openai

from security_models import (
    PayloadSafetyResult,
    PayloadSafetyFlag,
    compute_payload_hash,
)

OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_API_HOST = "api.openai.com"


def check_payload_safety(
    payload: str,
    api_key: Optional[str] = None,
) -> PayloadSafetyResult:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    payload_hash = compute_payload_hash(payload)

    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=payload,
    )

    result = response.results[0]
    is_safe = not result.flagged

    flags = []
    if result.flagged:
        categories = result.categories.model_dump()
        category_scores = result.category_scores.model_dump()

        for category_name, flagged in categories.items():
            if flagged and category_name != "flagged":
                score = category_scores.get(category_name, 0)
                severity = "high" if score > 0.8 else "medium" if score > 0.5 else "low"
                flags.append(
                    PayloadSafetyFlag(
                        category=category_name,
                        severity=severity,
                        description=f"Content flagged for {category_name} with score {score:.4f}",
                    )
                )

    return PayloadSafetyResult(
        payload_hash=payload_hash,
        is_safe=is_safe,
        flags=flags,
        analysis_timestamp=datetime.utcnow(),
    )


def check_payload_safety_detailed(
    payload: str,
    api_key: Optional[str] = None,
) -> Dict:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=payload,
    )

    result = response.results[0]
    categories = result.categories.model_dump()
    category_scores = result.category_scores.model_dump()

    return {
        "flagged": result.flagged,
        "categories": {k: v for k, v in categories.items() if k != "flagged" and v},
        "scores": {
            k: v for k, v in category_scores.items() if k != "flagged" and v > 0
        },
    }


def batch_check_payload_safety(
    payloads: List[str],
    api_key: Optional[str] = None,
) -> List[PayloadSafetyResult]:
    results = []
    for payload in payloads:
        result = check_payload_safety(payload, api_key=api_key)
        results.append(result)
    return results


def check_decrypted_payload_safety(
    decrypted_text: str,
    key_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> PayloadSafetyResult:
    result = check_payload_safety(decrypted_text, api_key=api_key)
    return result


def get_safety_report(
    payload: str,
    api_key: Optional[str] = None,
) -> str:
    result = check_payload_safety(payload, api_key=api_key)

    lines = [
        f"Payload Safety Report",
        f"=====================",
        f"Payload Hash: {result.payload_hash}",
        f"Analysis Time: {result.analysis_timestamp}",
        f"Overall Safe: {result.is_safe}",
        f"",
    ]

    if result.flags:
        lines.append("Flags:")
        for flag in result.flags:
            lines.append(
                f"  - [{flag.severity.upper()}] {flag.category}: {flag.description}"
            )
    else:
        lines.append("No safety flags detected.")

    return "\n".join(lines)
