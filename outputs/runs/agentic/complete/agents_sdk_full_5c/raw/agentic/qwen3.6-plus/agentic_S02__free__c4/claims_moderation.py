"""
Moderate free-text claims or notes using OpenAI Moderation API.

Provider: OpenAI Moderation API (https://platform.openai.com/docs/guides/moderation)
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field

import openai
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION", "")

# OpenAI moderation model identifier
MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "text-moderation-latest")
# Alternative model: "omni-moderation-latest"


@dataclass
class ModerationResult:
    """Result of content moderation check."""
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    text: str = ""
    model_used: str = ""


@dataclass
class ClaimModerationReport:
    """Full moderation report for federated login claims."""
    claim_id: str
    original_text: str
    moderated: bool
    moderation_result: Optional[ModerationResult] = None
    policy_violations: List[str] = field(default_factory=list)
    recommendation: str = "approve"  # approve, review, reject
    reviewed_at: int = 0


class ModerationError(Exception):
    """Raised when OpenAI moderation API call fails."""
    pass


def init_openai_client() -> OpenAI:
    """Initialize OpenAI client for moderation API calls."""
    client_kwargs = {"api_key": OPENAI_API_KEY}
    if OPENAI_ORGANIZATION:
        client_kwargs["organization"] = OPENAI_ORGANIZATION
    return OpenAI(**client_kwargs)


def moderate_text(text: str, model: str = MODERATION_MODEL) -> ModerationResult:
    """
    Moderate text using OpenAI Moderation API.

    Calls the /v1/moderations endpoint with the specified model.
    Uses text-moderation-latest for best accuracy and lowest false positives.
    """
    if not text or not text.strip():
        return ModerationResult(
            flagged=False,
            text=text,
            model_used=model,
        )

    try:
        client = init_openai_client()

        response = client.moderations.create(
            input=text,
            model=model,
        )

        result = response.results[0]

        categories = {}
        category_scores = {}

        for category, flagged in result.flagged:
            categories[category] = flagged

        # Get scores from the response
        if hasattr(result, 'category_scores'):
            for category, score in result.category_scores.items():
                category_scores[category] = score

        return ModerationResult(
            flagged=result.flagged,
            categories=categories,
            category_scores=category_scores,
            text=text,
            model_used=model,
        )

    except openai.APIError as e:
        raise ModerationError(f"OpenAI moderation API error: {str(e)}")
    except Exception as e:
        raise ModerationError(f"Moderation failed: {str(e)}")


def evaluate_policy_violations(moderation_result: ModerationResult) -> List[str]:
    """
    Evaluate which policy violations are present based on moderation categories.

    Maps OpenAI moderation categories to internal policy violation types.
    """
    violations = []

    category_mapping = {
        "hate": "Hate Speech Policy",
        "hate/threatening": "Threatening Hate Speech",
        "harassment": "Harassment Policy",
        "harassment/threatening": "Threatening Harassment",
        "self-harm": "Self-Harm Content Policy",
        "self-harm/intent": "Self-Harm Intent",
        "self-harm/instructions": "Self-Harm Instructions",
        "sexual": "Sexual Content Policy",
        "sexual/minors": "Minor Sexual Content",
        "violence": "Violence Policy",
        "violence/graphic": "Graphic Violence",
    }

    for category, flagged in moderation_result.categories.items():
        if flagged and category in category_mapping:
            violations.append(category_mapping[category])

    return violations


def moderate_federated_claim(
    claim_id: str,
    claim_text: str,
    custom_model: Optional[str] = None,
) -> ClaimModerationReport:
    """
    Moderate a federated login claim or user note.

    Uses OpenAI text-moderation-latest model to check for policy violations
    and returns a moderation recommendation.
    """
    model = custom_model or MODERATION_MODEL

    try:
        moderation_result = moderate_text(claim_text, model=model)
        violations = evaluate_policy_violations(moderation_result)

        # Determine recommendation
        if not moderation_result.flagged:
            recommendation = "approve"
        elif len(violations) > 2:
            recommendation = "reject"
        else:
            recommendation = "review"

        import time
        return ClaimModerationReport(
            claim_id=claim_id,
            original_text=claim_text,
            moderated=True,
            moderation_result=moderation_result,
            policy_violations=violations,
            recommendation=recommendation,
            reviewed_at=int(time.time()),
        )

    except ModerationError as e:
        return ClaimModerationReport(
            claim_id=claim_id,
            original_text=claim_text,
            moderated=False,
            recommendation="review",
            policy_violations=[f"Moderation error: {str(e)}"],
        )


def moderate_multiple_claims(
    claims: List[Dict[str, str]],
    model: str = MODERATION_MODEL,
) -> List[ClaimModerationReport]:
    """
    Moderate multiple claims in batch using OpenAI Moderation API.
    """
    results = []
    for claim in claims:
        claim_id = claim.get("id", "")
        claim_text = claim.get("text", claim.get("content", ""))
        result = moderate_federated_claim(claim_id, claim_text, custom_model=model)
        results.append(result)
    return results


if __name__ == "__main__":
    import json

    test_text = "This is a normal federated login note from the user."
    report = moderate_federated_claim("test-001", test_text)
    print(json.dumps({
        "claim_id": report.claim_id,
        "moderated": report.moderated,
        "flagged": report.moderation_result.flagged if report.moderation_result else None,
        "recommendation": report.recommendation,
        "violations": report.policy_violations,
    }, indent=2))
