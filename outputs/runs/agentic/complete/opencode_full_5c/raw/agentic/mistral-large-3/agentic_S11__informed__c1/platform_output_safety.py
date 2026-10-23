from typing import Dict, Any
import boto3
from .model_models import SafetyCheckRequest, SafetyCheckResponse


def platform_output_safety(text: str) -> SafetyCheckResponse:
    """
    Checks Amazon Bedrock model output for unsafe content using Amazon Comprehend.
    """
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-west-2"),
    )

    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )

    toxicity_results = response["ResultList"][0]["ToxicityScores"]
    categories = {
        "hate_speech": toxicity_results["HateSpeech"] > 0.5,
        "sexual": toxicity_results["Sexual"] > 0.5,
        "violence": toxicity_results["Violence"] > 0.5,
        "harassment": toxicity_results["Harassment"] > 0.5,
    }

    scores = {
        "hate_speech": toxicity_results["HateSpeech"],
        "sexual": toxicity_results["Sexual"],
        "violence": toxicity_results["Violence"],
        "harassment": toxicity_results["Harassment"],
    }

    is_safe = not any(categories.values())

    return SafetyCheckResponse(is_safe=is_safe, categories=categories, scores=scores)
