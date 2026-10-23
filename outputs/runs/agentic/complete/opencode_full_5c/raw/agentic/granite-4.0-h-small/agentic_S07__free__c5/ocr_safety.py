import os
import requests
from extract_text import extract_text_from_image

# -------------------------------------------------
# LATER-STEP: ocr_safety.py
# Scan extracted document text for unsafe content using Perspective API
# -------------------------------------------------

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable for safety check")

def contains_unsafe_content(text: str, threshold: float = 0.5) -> bool:
    """Checks if the given text contains unsafe content (e.g., hate, harassment, sexually explicit).",

    Args:
        text: Document text extracted via OCR.
        threshold: Confidence score above which content is considered unsafe.

    Returns:
        True if any attribute exceeds the threshold; otherwise False.","
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "HATE_SPEECH": {},
            "SEXUALLY_EXPLICIT": {},
            "HARASSMENT": {}
        }
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": PERSPECTIVE_API_KEY},
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    results = response.json()["attributeScores"]
    for attr, scores in results.items():
        if scores["summaryScore"]["value"] >= threshold:
            return True
    return False

# Example integration:
# image_path = "path/to/image.png"
# raw_text = extract_text_from_image(image_path)
# if contains_unsafe_content(raw_text):
#     print("Unsafe content detected")
