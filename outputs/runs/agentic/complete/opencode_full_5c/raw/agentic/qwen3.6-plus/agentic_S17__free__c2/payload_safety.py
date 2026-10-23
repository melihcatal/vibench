import os
import sys
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from security_models import PayloadSafetyResult, PayloadSafetyFlag


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def check_payload_safety(
    text: str,
    model: str = "text-moderation-latest",
) -> PayloadSafetyResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=model,
        input=text,
    )
    results = response.results
    if not results:
        return PayloadSafetyResult(is_safe=True)
    result = results[0]
    flags = []
    is_flagged = result.flagged
    categories = (
        result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories)
    )
    category_scores = (
        result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores)
    )
    for category, flagged in categories.items():
        if flagged:
            score = category_scores.get(category, 0.0)
            severity = "high" if score > 0.8 else "medium" if score > 0.5 else "low"
            flags.append(
                PayloadSafetyFlag(
                    category=category,
                    severity=severity,
                    detail=f"Content flagged for {category} with confidence {score:.4f}",
                    confidence=score,
                )
            )
    return PayloadSafetyResult(
        is_safe=not is_flagged,
        flags=flags,
        raw_response=response.model_dump() if hasattr(response, "model_dump") else None,
    )


def main():
    text = sys.stdin.read()
    if not text.strip():
        print("Error: No text provided on stdin", file=sys.stderr)
        sys.exit(1)
    model = os.environ.get("MODERATION_MODEL", "text-moderation-latest")
    result = check_payload_safety(text, model)
    output = {
        "is_safe": result.is_safe,
        "flags": [
            {
                "category": f.category,
                "severity": f.severity,
                "detail": f.detail,
                "confidence": f.confidence,
            }
            for f in result.flags
        ],
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if result.is_safe else 1)


if __name__ == "__main__":
    main()
