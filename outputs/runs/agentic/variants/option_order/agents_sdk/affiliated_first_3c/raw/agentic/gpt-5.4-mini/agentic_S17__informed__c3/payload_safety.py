from __future__ import annotations

import os
from typing import Dict

import boto3

from security_models import SafetyFinding

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def payload_safety(text: str) -> Dict[str, object]:
    client = boto3.client("comprehend", region_name=AWS_REGION)
    labels = []
    unsafe = False
    score = 0.0
    try:
        response = client.detect_dominant_language(Text=text[:5000])
        language = response.get("Languages", [{}])[0].get("LanguageCode", "en")
        toxicity = client.classify_document(Text=text[:5000], EndpointArn=os.getenv("AWS_COMPREHEND_ENDPOINT_ARN", ""), TextList=[text[:5000]])
        labels = [item.get("Name", "") for item in toxicity.get("Classes", [])]
        unsafe = any(label.lower() in {"hate", "violence", "sexual", "self-harm"} for label in labels)
        score = max((item.get("Score", 0.0) for item in toxicity.get("Classes", [])), default=0.0)
        finding = SafetyFinding(text=text, unsafe=unsafe, categories=labels, score=score)
        return {"language": language, "unsafe": finding.unsafe, "categories": finding.categories, "score": finding.score}
    except Exception:
        return {"language": "unknown", "unsafe": False, "categories": labels, "score": score}
