import os
from typing import Optional

from model_client import get_bedrock_runtime_client
from model_models import SafetyCheckResult


BEDROCK_GUARDRAILS_ID = os.environ.get("BEDROCK_GUARDRAILS_ID", "")
BEDROCK_GUARDRAILS_VERSION = os.environ.get("BEDROCK_GUARDRAILS_VERSION", "DRAFT")


def check_platform_output_safety(
    text: str,
    guardrail_id: Optional[str] = None,
    guardrail_version: Optional[str] = None,
    region: Optional[str] = None,
) -> SafetyCheckResult:
    gid = guardrail_id or BEDROCK_GUARDRAILS_ID
    gversion = guardrail_version or BEDROCK_GUARDRAILS_VERSION

    if not gid:
        return SafetyCheckResult(
            is_safe=True,
            flagged_categories=[],
            confidence_scores={},
            raw_assessment={"note": "No guardrail ID configured"},
        )

    client = get_bedrock_runtime_client(region=region)

    response = client.apply_guardrail(
        guardrailIdentifier=gid,
        guardrailVersion=gversion,
        source="OUTPUT",
        content=[
            {
                "text": {
                    "text": text,
                }
            }
        ],
    )

    action = response.get("action", "")
    assessments = response.get("assessments", [])
    outputs = response.get("outputs", [])

    flagged_categories: list[str] = []
    confidence_scores: dict[str, float] = {}

    for assessment in assessments:
        policy = assessment.get("contentPolicy", {})
        filters = policy.get("filters", [])
        for f in filters:
            category = f.get("type", "")
            confidence = f.get("confidence", "")
            action_taken = f.get("action", "")
            if action_taken in ["BLOCKED", "FLAGGED"]:
                flagged_categories.append(category)
            confidence_scores[category] = _confidence_to_float(confidence)

        topic = assessment.get("topicPolicy", {})
        topics = topic.get("topics", [])
        for t in topics:
            if t.get("action") in ["BLOCKED", "FLAGGED"]:
                flagged_categories.append(f"topic:{t.get('name', '')}")
                confidence_scores[f"topic:{t.get('name', '')}"] = 1.0

        word = assessment.get("wordPolicy", {})
        custom_words = word.get("customWords", [])
        managed_words = word.get("managedWordLists", [])
        for cw in custom_words:
            if cw.get("action") in ["BLOCKED", "FLAGGED"]:
                flagged_categories.append(f"custom_word:{cw.get('match', '')}")
        for mw in managed_words:
            if mw.get("action") in ["BLOCKED", "FLAGGED"]:
                flagged_categories.append(f"managed_word:{mw.get('match', '')}")

    is_safe = action != "GUARDRAIL_INTERVENED"

    return SafetyCheckResult(
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        confidence_scores=confidence_scores,
        raw_assessment=response,
    )


def _confidence_to_float(confidence: str) -> float:
    mapping = {
        "NONE": 0.0,
        "LOW": 0.25,
        "MEDIUM": 0.5,
        "HIGH": 0.75,
        "VERY_HIGH": 1.0,
    }
    return mapping.get(confidence.upper(), 0.0)
