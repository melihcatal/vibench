"""
claims_moderation.py - Moderate free-text claims or notes from federated identity profiles
Provider: OpenAI (openai.com) - GPT-4 model with moderation endpoint
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from openai import OpenAI


OPENAI_MODEL = "gpt-4"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def moderate_claim_text(
    claim_text: str,
    context: str = "federated identity profile",
    model: str = OPENAI_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text claims using OpenAI moderation and GPT-4 analysis.

    Provider: OpenAI (openai.com)
    Models: text-moderation-latest, gpt-4
    """
    effective_api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not effective_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=effective_api_key)

    # Step 1: Run OpenAI content moderation
    moderation_response = client.moderations.create(
        input=claim_text,
        model=OPENAI_MODERATION_MODEL,
    )

    moderation_result = moderation_response.results[0]
    flagged = moderation_result.flagged
    categories = moderation_result.categories.model_dump()
    category_scores = moderation_result.category_scores.model_dump()

    # Step 2: If flagged or for detailed analysis, use GPT-4 for contextual review
    analysis = None
    if flagged or True:  # Always analyze for identity context
        analysis_prompt = (
            f"Review the following user-provided text from a {context} field "
            f"and determine if it is appropriate for storage in an identity profile.\n\n"
            f"Text: {claim_text}\n\n"
            f"Consider:\n"
            f"- Does it contain PII beyond what is expected?\n"
            f"- Is it offensive, harmful, or abusive?\n"
            f"- Does it contain code injection attempts?\n"
            f"- Is it relevant to an identity profile context?\n\n"
            f"Respond with JSON containing:\n"
            f'- "appropriate": true/false\n'
            f'- "reason": brief explanation\n'
            f'- "action": "approve" | "flag" | "reject"\n'
            f'- "confidence": 0.0-1.0'
        )

        analysis_response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an identity profile content moderator. "
                        "Evaluate user-provided text for appropriateness in identity systems."
                    ),
                },
                {"role": "user", "content": analysis_prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        analysis_text = analysis_response.choices[0].message.content.strip()
        analysis = analysis_text

    return {
        "success": True,
        "text_length": len(claim_text),
        "moderation_flagged": flagged,
        "moderation_categories": categories,
        "category_scores": category_scores,
        "gpt4_analysis": analysis,
        "model": model,
        "provider": "openai",
        "reviewed_at": datetime.utcnow().isoformat(),
    }


def batch_moderate_claims(
    claims: List[Dict[str, str]],
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderately multiple claim texts using OpenAI.

    Each claim dict should have: {"field_name": "...", "value": "..."}

    Provider: OpenAI
    """
    results = []
    for claim in claims:
        field_name = claim.get("field_name", "unknown")
        value = claim.get("value", "")

        if not value:
            results.append({
                "field_name": field_name,
                "success": True,
                "moderation_flagged": False,
                "skipped": True,
                "reason": "Empty value",
            })
            continue

        result = moderate_claim_text(value, context=f"federated identity {field_name}", api_key=api_key)
        result["field_name"] = field_name
        results.append(result)

    return results
