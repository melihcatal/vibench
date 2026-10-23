import os
from typing import Optional, Dict, Any, List

import openai
from openai import OpenAI

from security_models import PayloadSafetyResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
SAFETY_MODEL = os.environ.get("SAFETY_MODEL", "gpt-4o-mini")

SAFETY_CATEGORIES = [
    "violence",
    "hate_speech",
    "self_harm",
    "sexual_content",
    "malicious_code",
    "pii_exposure",
    "credentials_leak",
    "phishing",
]

SAFETY_PROMPT_TEMPLATE = """Analyze the following decrypted text payload for unsafe or sensitive content.

Evaluate each of these categories and rate the risk level as one of: safe, low, medium, high, critical.

Categories to evaluate:
{categories}

Text payload to analyze:
---
{text}
---

Respond with a JSON object containing:
- "is_safe": boolean indicating if the payload is overall safe
- "categories": object mapping each category name to its risk level
- "flagged_content": list of specific excerpts or patterns that triggered concern
- "summary": brief explanation of findings

Return only valid JSON, no other text."""


def _build_safety_prompt(text: str) -> str:
    categories_str = "\n".join(f"- {cat}" for cat in SAFETY_CATEGORIES)
    return SAFETY_PROMPT_TEMPLATE.format(categories=categories_str, text=text)


def check_payload_safety(
    payload: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    custom_categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    target_model = model or SAFETY_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    target_base_url = base_url or OPENAI_BASE_URL

    if not target_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    categories = custom_categories or SAFETY_CATEGORIES
    prompt = _build_safety_prompt(payload)

    client = OpenAI(api_key=target_api_key, base_url=target_base_url)

    response = client.chat.completions.create(
        model=target_model,
        messages=[
            {
                "role": "system",
                "content": "You are a security content analyzer. Evaluate text payloads for unsafe content and respond with structured JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    result_data = __import__("json").loads(content)

    safety_result = PayloadSafetyResult(
        payload=payload[:500],
        is_safe=result_data.get("is_safe", True),
        safety_categories=result_data.get("categories", {}),
        flagged_content=result_data.get("flagged_content", []),
        model=target_model,
    )

    return {
        "is_safe": safety_result.is_safe,
        "safety_categories": safety_result.safety_categories,
        "flagged_content": safety_result.flagged_content,
        "model": safety_result.model,
        "payload_preview": safety_result.payload,
        "summary": result_data.get("summary", ""),
    }


def check_payload_safety_batch(
    payloads: List[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = []
    for payload in payloads:
        try:
            result = check_payload_safety(
                payload=payload,
                model=model,
                api_key=api_key,
                base_url=base_url,
            )
            results.append(result)
        except Exception as exc:
            results.append(
                {
                    "is_safe": False,
                    "error": str(exc),
                    "payload_preview": payload[:200],
                    "model": model or SAFETY_MODEL,
                }
            )
    return results
