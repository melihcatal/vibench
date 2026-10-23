from typing import Dict, List

import boto3


def visual_safety_text(labels: List[str]) -> Dict[str, object]:
    client = boto3.client("comprehend")
    text = " ".join(labels)
    response = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"provider": "aws.comprehend", "sentiment": response.get("Sentiment", ""), "scores": response.get("SentimentScore", {})}
