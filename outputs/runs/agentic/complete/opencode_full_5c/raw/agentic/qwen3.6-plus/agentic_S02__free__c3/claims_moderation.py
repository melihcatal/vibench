import os
import time
from typing import Any, Dict, List, Optional

import openai

from identity_models import ModerationResult, AuditEvent, AuditEventType


OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def get_openai_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def moderate_federated_claims(
    claims_text: str,
    user_id: Optional[str] = None,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_openai_client()

    moderation_response = client.moderations.create(
        model="omni-moderation-latest",
        input=claims_text,
    )

    result = moderation_response.results[0]
    categories = {}
    category_scores = {}

    for cat, flagged in result.categories.model_dump().items():
        categories[cat] = flagged

    for cat, score in result.category_scores.model_dump().items():
        category_scores[cat] = score

    is_flagged = result.flagged

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.CLAIMS_MODERATED,
        timestamp=time.time(),
        user_id=user_id,
        provider=provider or "openai",
        details={
            "flagged": is_flagged,
            "categories_checked": list(categories.keys()),
            "model": "omni-moderation-latest",
        },
        status="flagged" if is_flagged else "cleared",
    )

    return {
        "success": True,
        "moderation": ModerationResult(
            flagged=is_flagged,
            categories=categories,
            category_scores=category_scores,
            raw_response=result.model_dump(),
        ).__dict__,
        "audit_event": audit_event.to_dict(),
        "provider": "openai",
        "model": "omni-moderation-latest",
    }


def analyze_claims_content(
    claims_text: str,
    user_id: Optional[str] = None,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_openai_client()

    system_prompt = """You are an identity verification assistant. Analyze the provided user claims or profile notes for:
1. Consistency issues (contradictory information)
2. Suspicious patterns (potential fraud indicators)
3. Data quality issues (missing or malformed fields)
4. Risk level assessment (low, medium, high)

Return a structured JSON analysis."""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Analyze these federated login claims:\n{claims_text}",
            },
        ],
        temperature=0.1,
        max_tokens=500,
    )

    analysis_text = response.choices[0].message.content

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.CLAIMS_MODERATED,
        timestamp=time.time(),
        user_id=user_id,
        provider="openai",
        details={
            "analysis_type": "content_analysis",
            "model": OPENAI_MODEL,
        },
    )

    return {
        "success": True,
        "analysis": analysis_text,
        "audit_event": audit_event.to_dict(),
        "provider": "openai",
        "model": OPENAI_MODEL,
    }


def moderate_claims_batch(
    claims_list: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    results = []
    for claim_entry in claims_list:
        text = claim_entry.get("text", "")
        user_id = claim_entry.get("user_id")
        provider = claim_entry.get("provider")

        result = moderate_federated_claims(
            claims_text=text,
            user_id=user_id,
            provider=provider,
        )
        results.append(result)

    return results


def validate_claim_safety(
    claim_value: str,
    field_name: str,
) -> Dict[str, Any]:
    client = get_openai_client()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You validate whether a user-provided claim value for an identity field "
                    "is safe and appropriate. Check for PII leakage, injection attempts, "
                    "or inappropriate content. Return JSON with: safe (bool), reason (str), risk_level (str)."
                ),
            },
            {
                "role": "user",
                "content": f"Field: {field_name}\nValue: {claim_value}\nIs this safe to store in an identity profile?",
            },
        ],
        temperature=0.0,
        max_tokens=200,
    )

    validation_text = response.choices[0].message.content

    return {
        "field": field_name,
        "validation": validation_text,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
