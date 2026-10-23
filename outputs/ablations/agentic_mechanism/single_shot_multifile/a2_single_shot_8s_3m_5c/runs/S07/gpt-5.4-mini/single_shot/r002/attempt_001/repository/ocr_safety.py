from typing import Dict

import boto3

from document_models import OcrResult


def check_unsafe_content(result: OcrResult) -> Dict[str, object]:
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=result.text[:4500], LanguageCode="en")
    unsafe = response.get("Sentiment") in {"NEGATIVE", "MIXED"}
    return {"unsafe": unsafe, "sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}
