import os
import json
from typing import Dict, Any, List, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_user_claims_with_azure(
    content: str, claim_type: str = "user_profile"
) -> Dict[str, Any]:
    """
    Moderate free-text claims or notes using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Request to analyze text
    request = AnalyzeTextOptions(text=content)

    try:
        # Analyze text for safety
        response = client.analyze_text(request)

        # Process results
        hate_result = None
        self_harm_result = None
        sexual_result = None
        violence_result = None

        for category_result in response.categories_analysis:
            if category_result.category == TextCategory.HATE:
                hate_result = category_result
            elif category_result.category == TextCategory.SELF_HARM:
                self_harm_result = category_result
            elif category_result.category == TextCategory.SEXUAL:
                sexual_result = category_result
            elif category_result.category == TextCategory.VIOLENCE:
                violence_result = category_result

        # Determine if content is safe
        is_safe = True
        reasons = []

        # Check each category against threshold (severity 2 or higher is problematic)
        threshold = 2

        if hate_result and hate_result.severity >= threshold:
            is_safe = False
            reasons.append(f"Hate content detected (severity: {hate_result.severity})")

        if self_harm_result and self_harm_result.severity >= threshold:
            is_safe = False
            reasons.append(
                f"Self-harm content detected (severity: {self_harm_result.severity})"
            )

        if sexual_result and sexual_result.severity >= threshold:
            is_safe = False
            reasons.append(
                f"Sexual content detected (severity: {sexual_result.severity})"
            )

        if violence_result and violence_result.severity >= threshold:
            is_safe = False
            reasons.append(
                f"Violence content detected (severity: {violence_result.severity})"
            )

        # Calculate overall confidence (inverse of max severity normalized)
        max_severity = max(
            hate_result.severity if hate_result else 0,
            self_harm_result.severity if self_harm_result else 0,
            sexual_result.severity if sexual_result else 0,
            violence_result.severity if violence_result else 0,
        )
        confidence = max(0, 1 - (max_severity / 7))  # Severity scale is 0-7

        result = {
            "is_approved": is_safe,
            "confidence": confidence,
            "reasons": reasons if not is_safe else ["Content is safe"],
            "category_scores": {
                "hate": hate_result.severity if hate_result else 0,
                "self_harm": self_harm_result.severity if self_harm_result else 0,
                "sexual": sexual_result.severity if sexual_result else 0,
                "violence": violence_result.severity if violence_result else 0,
            },
            "provider": "azure_content_safety",
            "claim_type": claim_type,
        }

        return result

    except Exception as e:
        # Fallback to basic moderation if Azure service fails
        return basic_text_moderation(content, claim_type)


def moderate_multiple_claims(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Moderate multiple claims in batch.
    Each claim should have 'text' and 'claim_type' fields.
    """
    results = []
    for claim in claims:
        text = claim.get("text", "")
        claim_type = claim.get("claim_type", "user_profile")
        user_id = claim.get("user_id")

        moderation_result = moderate_user_claims_with_azure(text, claim_type)

        # Add user context if available
        if user_id:
            moderation_result["user_id"] = user_id

        results.append(moderation_result)

    return results


def basic_text_moderation(content: str, claim_type: str) -> Dict[str, Any]:
    """
    Basic text moderation as fallback when Azure service is unavailable.
    """
    # Simple keyword-based moderation
    problematic_keywords = [
        # Hate speech
        "hate",
        "racist",
        "sexist",
        "bigot",
        # Self-harm
        "suicide",
        "self harm",
        "kill myself",
        # Sexual content
        "porn",
        "xxx",
        "adult content",
        # Violence
        "kill",
        "murder",
        "violence",
        "attack",
    ]

    content_lower = content.lower()
    found_keywords = []

    for keyword in problematic_keywords:
        if keyword in content_lower:
            found_keywords.append(keyword)

    is_safe = len(found_keywords) == 0

    result = {
        "is_approved": is_safe,
        "confidence": 0.7 if is_safe else 0.3,  # Lower confidence for basic moderation
        "reasons": [f"Contains problematic keywords: {', '.join(found_keywords)}"]
        if not is_safe
        else ["Basic check passed"],
        "category_scores": {
            "hate": 1
            if any(kw in ["hate", "racist", "sexist", "bigot"] for kw in found_keywords)
            else 0,
            "self_harm": 1
            if any(
                kw in ["suicide", "self harm", "kill myself"] for kw in found_keywords
            )
            else 0,
            "sexual": 1
            if any(kw in ["porn", "xxx", "adult content"] for kw in found_keywords)
            else 0,
            "violence": 1
            if any(
                kw in ["kill", "murder", "violence", "attack"] for kw in found_keywords
            )
            else 0,
        },
        "provider": "basic_fallback",
        "claim_type": claim_type,
        "note": "Azure Content Safety service unavailable, using basic keyword check",
    }

    return result


def should_escalate_for_review(moderation_result: Dict[str, Any]) -> bool:
    """
    Determine if a moderation result should be escalated for human review.
    """
    # Escalate if confidence is low or if there are multiple categories flagged
    if moderation_result.get("confidence", 1) < 0.5:
        return True

    # Count how many categories have severity > 0
    category_scores = moderation_result.get("category_scores", {})
    flagged_categories = sum(1 for score in category_scores.values() if score > 0)

    if flagged_categories >= 2:
        return True

    # Escalate if hate or violence content is detected with moderate severity
    if category_scores.get("hate", 0) >= 3 or category_scores.get("violence", 0) >= 3:
        return True

    return False
