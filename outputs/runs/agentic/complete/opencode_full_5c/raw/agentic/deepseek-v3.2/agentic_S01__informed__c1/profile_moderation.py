import os
import boto3
from botocore.config import Config
from typing import Dict, Any


def moderate_profile_text(text: str) -> Dict[str, Any]:
    """Moderate profile text before account activation using Amazon Comprehend."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    comprehend_client = boto3.client("comprehend", config=config)

    try:
        response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        results = response["ResultList"][0]
        toxicity_scores = results["Toxicity"]

        max_toxicity = max(score["Score"] for score in toxicity_scores)

        is_toxic = max_toxicity > 0.5

        moderation_result = {
            "is_approved": not is_toxic,
            "toxicity_score": max_toxicity,
            "scores": {score["Label"]: score["Score"] for score in toxicity_scores},
            "text_length": len(text),
            "moderation_reason": "Toxic content detected"
            if is_toxic
            else "Content is clean",
        }

        return moderation_result
    except Exception as e:
        print(f"Moderation failed: {e}")
        return {
            "is_approved": True,
            "toxicity_score": 0.0,
            "scores": {},
            "text_length": len(text),
            "moderation_reason": "Moderation service unavailable",
        }


def moderate_user_profile(profile_data: Dict[str, str]) -> Dict[str, Any]:
    """Moderate all text fields in a user profile."""
    all_text = " ".join(str(value) for value in profile_data.values() if value)

    moderation_result = moderate_profile_text(all_text)

    if not moderation_result["is_approved"]:
        moderation_result["flagged_fields"] = [
            key for key, value in profile_data.items() if value and len(str(value)) > 0
        ]

    return moderation_result


def check_content_safety(text: str) -> bool:
    """Check if text passes content safety guidelines."""
    result = moderate_profile_text(text)
    return result["is_approved"]
