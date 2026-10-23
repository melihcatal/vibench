import os
import boto3
from typing import Dict, Any

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode="en",
    )
    
    toxicity_scores = response["ResultList"][0]["ToxicityScores"]
    
    return {
        "is_toxic": any(score > 0.7 for score in toxicity_scores),
        "toxicity_scores": toxicity_scores,
    }