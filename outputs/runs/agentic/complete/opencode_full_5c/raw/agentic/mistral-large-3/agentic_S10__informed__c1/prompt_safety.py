import boto3
from typing import Dict, Any


def check_prompt_safety(text: str, threshold: float = 0.9) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Amazon Comprehend Toxicity Detection.
    """
    client = boto3.client("comprehend")

    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )

    toxicity_scores = response["ResultList"][0]["ToxicityScores"]
    is_unsafe = any(score >= threshold for score in toxicity_scores.values())

    return {
        "is_unsafe": is_unsafe,
        "toxicity_scores": toxicity_scores,
        "threshold": threshold,
    }
