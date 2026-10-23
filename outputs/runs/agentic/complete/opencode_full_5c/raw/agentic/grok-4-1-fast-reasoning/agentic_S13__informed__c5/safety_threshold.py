import boto3
import os
from typing import Dict, List, Any
from safety_client import get_thresholds
from safety_models import SafetyScore


def safety_threshold(
    text: str, custom_thresholds: Dict[str, float] = None
) -> Dict[str, Any]:
    thresholds = custom_thresholds or get_thresholds()

    comprehend = boto3.client("comprehend", region_name="us-west-2")
    response = comprehend.detect_toxicity(Text=text, LanguageCode="en")

    labels = response["Result"]["Labels"]
    scores: List[SafetyScore] = [
        {"category": label["Name"].lower(), "score": label["Score"]} for label in labels
    ]

    flagged: List[str] = [
        s["category"] for s in scores if s["score"] > thresholds.get(s["category"], 0.5)
    ]

    return {
        "input_text": text,
        "allowed": len(flagged) == 0,
        "scores": scores,
        "flagged_categories": flagged,
        "thresholds_used": thresholds,
    }
