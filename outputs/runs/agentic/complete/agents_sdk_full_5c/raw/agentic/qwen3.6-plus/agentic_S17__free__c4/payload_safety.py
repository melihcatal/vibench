"""
Check decrypted text payloads for unsafe content using the OpenAI Moderation API.
Uses the openai python SDK to call the text-moderation-latest model for
detecting harmful, unsafe, or policy-violating content in payloads.

Provider: OpenAI Moderation API - api.openai.com
Model: text-moderation-latest
"""

import json
import logging
import os
from typing import Optional, Dict, Any, List

from openai import OpenAI

from security_models import SafetyCheckRequest, SafetyCheckResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Moderation API model identifier
OPENAI_MODERATION_MODEL = "text-moderation-latest"

# Thresholds for flagging categories
DEFAULT_FLAG_THRESHOLD = 0.5


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for moderation API calls.
    Provider: OpenAI - api.openai.com
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def check_payload_safety(
    text: str,
    attributes: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    flag_threshold: float = DEFAULT_FLAG_THRESHOLD,
) -> SafetyCheckResponse:
    """
    Check a decrypted text payload for unsafe content using OpenAI Moderation API.

    Provider: OpenAI Moderation API - api.openai.com
    Model: text-moderation-latest

    Categories checked by OpenAI moderation:
    - hate, hate/threatening
    - harassment, harassment/threatening
    - self-harm, self-harm/intent, self-harm/instructions
    - sexual, sexual/minors
    - violence, violence/graphic

    Args:
        text: The decrypted text to check.
        attributes: Optional list of specific categories to check.
        api_key: Optional OpenAI API key override.
        flag_threshold: Score threshold for flagging (default: 0.5).

    Returns:
        SafetyCheckResponse with safety assessment and category scores.
    """
    request = SafetyCheckRequest(text=text, attributes=attributes)
    normalized_text = request.to_normalized_text()

    if not normalized_text:
        return SafetyCheckResponse(is_safe=True, attributes={})

    client = create_openai_client(api_key)

    try:
        logger.info("Checking payload safety with OpenAI Moderation API (model=%s)",
                     OPENAI_MODERATION_MODEL)

        moderation_result = client.moderations.create(
            input=normalized_text,
            model=OPENAI_MODERATION_MODEL,
        )

        result_entry = moderation_result.results[0]
        categories = result_entry.categories.model_dump()
        category_scores = result_entry.category_scores.model_dump()

        # Determine overall safety
        is_flagged = result_entry.flagged
        attribute_scores = {}

        for cat_name, score in category_scores.items():
            if score is None:
                continue
            if attributes and cat_name not in attributes:
                continue
            attribute_scores[cat_name] = round(score, 6)
            if score > flag_threshold:
                is_flagged = True

        response = SafetyCheckResponse(
            is_safe=not is_flagged,
            attributes=attribute_scores,
        )

        logger.info("Safety check complete: is_safe=%s, flags=%s",
                     response.is_safe, result_entry.flagged)
        return response

    except Exception as e:
        logger.error("OpenAI Moderation API error: %s", e)
        # Return safe=False on API failure to be conservative
        return SafetyCheckResponse(is_safe=False, attributes={})


def check_batch_safety(
    texts: List[str],
    api_key: Optional[str] = None,
) -> List[SafetyCheckResponse]:
    """
    Check multiple text payloads for safety in batch.

    Provider: OpenAI Moderation API - api.openai.com
    Model: text-moderation-latest

    Args:
        texts: List of text payloads to check.
        api_key: Optional API key override.

    Returns:
        List of SafetyCheckResponse objects.
    """
    client = create_openai_client(api_key)

    try:
        logger.info("Batch safety check for %d texts with OpenAI Moderation API", len(texts))

        moderation_result = client.moderations.create(
            input=texts,
            model=OPENAI_MODERATION_MODEL,
        )

        responses = []
        for idx, result_entry in enumerate(moderation_result.results):
            category_scores = result_entry.category_scores.model_dump()
            scores = {k: round(v, 6) for k, v in category_scores.items() if v is not None}
            responses.append(
                SafetyCheckResponse(
                    is_safe=not result_entry.flagged,
                    attributes=scores,
                )
            )

        return responses

    except Exception as e:
        logger.error("OpenAI batch moderation error: %s", e)
        return [SafetyCheckResponse(is_safe=False) for _ in texts]


def generate_safety_report(responses: List[SafetyCheckResponse]) -> Dict[str, Any]:
    """
    Generate an aggregate safety report from multiple checks.

    Args:
        responses: List of SafetyCheckResponse objects.

    Returns:
        Dict with summary statistics.
    """
    total = len(responses)
    safe_count = sum(1 for r in responses if r.is_safe)
    unsafe_count = total - safe_count

    # Aggregate max scores per category
    max_scores: Dict[str, float] = {}
    for resp in responses:
        for cat, score in resp.attributes.items():
            if cat not in max_scores or score > max_scores[cat]:
                max_scores[cat] = score

    return {
        "total_checked": total,
        "safe_count": safe_count,
        "unsafe_count": unsafe_count,
        "safety_rate": safe_count / total if total > 0 else 0.0,
        "max_category_scores": max_scores,
    }


if __name__ == "__main__":
    sample_text = "This is a normal decrypted payload with no unsafe content."
    result = check_payload_safety(sample_text)
    print(result.to_dict())
