"""
secret_label_safety.py - Check secret labels and notes for unsafe text using OpenAI.

Uses the OpenAI API (api.openai.com) with gpt-4o-mini to analyze secret
labels and notes for potentially unsafe content such as hardcoded credentials,
PII, or policy violations.
"""

from __future__ import annotations

import logging
import os
from typing import Optional, Dict, Any

from openai import OpenAI

from security_models import SafetyCheckResult

logger = logging.getLogger(__name__)

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url=OPENAI_API_BASE)


SAFETY_SYSTEM_PROMPT = """You are a security compliance assistant. Analyze the provided secret label or note text
and determine if it contains unsafe content. Unsafe content includes:
- Hardcoded passwords, API keys, or tokens
- Personally identifiable information (PII) such as SSNs, credit card numbers, or email addresses
- Internal hostnames, IP addresses, or infrastructure details that should not be in labels
- Anything that violates the principle of least privilege or secret management best practices

Respond with a JSON object containing:
- "is_safe": boolean
- "confidence": float between 0.0 and 1.0
- "flagged_terms": list of specific terms that are unsafe (empty if safe)
- "explanation": brief explanation of the safety assessment

Respond ONLY with valid JSON."""


def check_label_safety(
    secret_name: str,
    label_text: str,
    model: str = OPENAI_MODEL,
) -> SafetyCheckResult:
    """
    Check a secret label or note for unsafe content using OpenAI GPT-4o-mini.

    Args:
        secret_name: The name of the secret being checked.
        label_text: The label or note text to analyze.
        model: OpenAI model identifier (default: gpt-4o-mini).

    Returns:
        SafetyCheckResult with safety assessment.
    """
    client = get_openai_client()
    logger.info("Checking label safety for %s using OpenAI %s", secret_name, model)

    prompt = f"Analyze this secret label/note text for unsafe content:\n\n{label_text}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SAFETY_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=512,
        )

        content = response.choices[0].message.content or "{}"
        import json
        result_data = json.loads(content)

        safety_result = SafetyCheckResult(
            secret_name=secret_name,
            is_safe=result_data.get("is_safe", True),
            confidence=float(result_data.get("confidence", 0.0)),
            flagged_terms=result_data.get("flagged_terms", []),
            explanation=result_data.get("explanation", ""),
        )

        logger.info(
            "Safety check for %s: safe=%s, confidence=%.2f",
            secret_name,
            safety_result.is_safe,
            safety_result.confidence,
        )
        return safety_result

    except Exception as e:
        logger.error("OpenAI safety check failed for %s: %s", secret_name, e)
        return SafetyCheckResult(
            secret_name=secret_name,
            is_safe=False,
            confidence=0.0,
            explanation=f"Safety check failed: {str(e)}",
        )


def batch_check_labels(
    labels: Dict[str, str],
    model: str = OPENAI_MODEL,
) -> Dict[str, SafetyCheckResult]:
    """
    Check multiple secret labels for unsafe content.

    Args:
        labels: Dict mapping secret names to label text.
        model: OpenAI model identifier.

    Returns:
        Dict mapping secret names to SafetyCheckResult.
    """
    results = {}
    for secret_name, label_text in labels.items():
        results[secret_name] = check_label_safety(secret_name, label_text, model=model)
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_labels = {
        "db-credentials": "Primary DB password: super_secret_123! host=10.0.1.50",
        "api-key-prod": "Production Stripe key - rotate quarterly",
    }
    results = batch_check_labels(test_labels)
    for name, result in results.items():
        print(f"{name}: safe={result.is_safe}, flagged={result.flagged_terms}")
