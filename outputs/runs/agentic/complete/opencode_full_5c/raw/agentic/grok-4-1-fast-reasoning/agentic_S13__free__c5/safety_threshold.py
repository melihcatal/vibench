import os
from typing import Dict, Optional
from huggingface_hub import InferenceClient
from safety_models import ModerationResult
from safety_client import SAFETY_CONFIG


def safety_threshold(
    text: str, custom_thresholds: Optional[Dict[str, float]] = None
) -> ModerationResult:
    client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
    classification = client.text_classification(model="unitary/toxic-bert", inputs=text)
    categories = {item["label"].lower(): item["score"] for item in classification}
    thresholds = custom_thresholds or SAFETY_CONFIG["default_thresholds"]
    flagged = any(
        categories.get(cat, 0.0) > thresholds.get(cat, 0.5) for cat in categories
    )
    return {
        "input_text": text,
        "flagged": flagged,
        "categories": categories,
        "rationale": "Applied category thresholds",
    }
