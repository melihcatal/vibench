from __future__ import annotations

import os
from typing import Any

import boto3


COMPREHEND_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def check_annotation_safety(
    text: str,
    client: boto3.client | None = None,
) -> dict[str, Any]:
    if client is None:
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
        aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        if not aws_access_key or not aws_secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )
        client = boto3.client(
            "comprehend",
            region_name=COMPREHEND_REGION,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    result: dict[str, Any] = {
        "text": text,
        "safe": True,
        "toxicity_detections": [],
        "pii_detections": [],
        "sentiment": None,
    }

    try:
        sentiment_resp = client.detect_sentiment(Text=text, LanguageCode="en")
        result["sentiment"] = sentiment_resp.get("Sentiment", "UNKNOWN")
    except client.exceptions.TextSizeLimitExceededException:
        result["sentiment"] = "SKIPPED_TOO_LONG"
    except Exception:
        result["sentiment"] = "ERROR"

    try:
        pii_resp = client.detect_pii_entities(Text=text, LanguageCode="en")
        entities = pii_resp.get("Entities", [])
        if entities:
            result["safe"] = False
            result["pii_detections"] = [
                {
                    "type": e["Type"],
                    "score": e["Score"],
                    "text": text[e["BeginOffset"] : e["EndOffset"]],
                }
                for e in entities
            ]
    except client.exceptions.TextSizeLimitExceededException:
        result["pii_detections"] = [{"type": "SKIPPED", "score": 0.0, "text": ""}]
    except Exception:
        pass

    toxic_keywords = [
        "abuse",
        "malicious",
        "hack",
        "exploit",
        "vulnerability",
        "attack",
    ]
    text_lower = text.lower()
    for kw in toxic_keywords:
        if kw in text_lower:
            result["safe"] = False
            result["toxicity_detections"].append(
                {"keyword": kw, "flag": "potentially_harmful"}
            )

    return result


if __name__ == "__main__":
    import json

    sample = "This metric tracks user login failures on the production database server."
    result = check_annotation_safety(sample)
    print(json.dumps(result, indent=2))
