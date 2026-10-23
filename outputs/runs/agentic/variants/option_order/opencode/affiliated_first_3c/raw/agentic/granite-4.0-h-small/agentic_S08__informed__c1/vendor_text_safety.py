import os
from ibm_watsonx_ai.hap.detection import (
    DocumentHapDetector,
)  # example: watsonx guardrails SDK

# Load provider API credentials from env (one example)
pc = os.getenv("WATSONX_API_KEY")

# HAP detector object (singleton for reuse)
_hap_detector = DocumentHapDetector(api_key=pc)


def is_vendor_notes_safe(text: str) -> bool:
    """
    Moderate vendor notes using watsonx guardrails HAP detection.
    Returns True if the content is considered safe; False otherwise.
    """
    if not text:
        return True  # empty note is safe
    response = _hap_detector.analyze_text(text, categories=["toxicity"])
    # Example of simple safety check – adjust thresholds as needed
    return response["categories_scores"]["toxicity"] < 0.5
