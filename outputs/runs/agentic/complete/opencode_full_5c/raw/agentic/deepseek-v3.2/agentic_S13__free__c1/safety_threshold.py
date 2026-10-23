import os
from typing import Dict, Any, Optional
from safety_client import SafetyClient
from safety_models import SafetyThresholds


def safety_threshold(
    text: str, thresholds: Optional[SafetyThresholds] = None
) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text.

    Args:
        text: The text to evaluate
        thresholds: Optional custom thresholds, uses defaults if not provided

    Returns:
        Dictionary with threshold evaluation results
    """
    client = SafetyClient.get_client()

    if thresholds is None:
        thresholds = SafetyThresholds.get_default()

    # Use Amazon Comprehend for content moderation
    import boto3

    comprehend = boto3.client(
        "comprehend",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Detect toxic content
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )

    results = response["ResultList"][0]

    # Apply thresholds
    category_scores = {}
    category_decisions = {}
    overall_decision = "ALLOW"
    blocked_categories = []

    for toxicity in results["Toxicity"]:
        category = toxicity["Name"]
        score = toxicity["Score"]
        category_scores[category] = score

        # Get threshold for this category
        threshold = thresholds.get_threshold(category)

        # Make decision
        if score >= threshold:
            category_decisions[category] = "BLOCK"
            overall_decision = "BLOCK"
            blocked_categories.append(category)
        else:
            category_decisions[category] = "ALLOW"

    # Check if any category exceeds threshold
    if overall_decision == "BLOCK":
        action = "BLOCK"
        reason = f"Blocked categories: {', '.join(blocked_categories)}"
    else:
        action = "ALLOW"
        reason = "All categories below thresholds"

    return {
        "text": text,
        "action": action,
        "overall_decision": overall_decision,
        "category_scores": category_scores,
        "category_decisions": category_decisions,
        "blocked_categories": blocked_categories,
        "thresholds": thresholds.to_dict(),
        "reason": reason,
        "provider": "aws_comprehend",
        "model": "comprehend-toxic-detection",
    }
