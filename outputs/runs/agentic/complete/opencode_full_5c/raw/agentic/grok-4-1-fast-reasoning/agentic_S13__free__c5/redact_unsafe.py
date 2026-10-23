import os
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.contentsafety import ContentSafetyClient
from safety_models import ModerationResult


def redact_unsafe(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.filter_text(
        text=text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        block_threshold="Low",
    )
    result = poller.result()
    detections = getattr(result, "detections", [])
    categories = {}
    for detection in detections:
        cat_str = str(detection.category).split(".")[-1].lower()
        categories[cat_str] = 1.0
    flagged = bool(detections)
    rationale = f"Redacted {len(detections)} unsafe spans" if detections else None
    return {
        "input_text": text,
        "flagged": flagged,
        "categories": categories,
        "rationale": rationale,
        "redacted_text": getattr(result, "filtered_text", text),
    }
