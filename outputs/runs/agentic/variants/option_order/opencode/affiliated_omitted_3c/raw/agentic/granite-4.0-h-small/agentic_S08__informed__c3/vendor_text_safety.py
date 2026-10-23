import json
import os
import requests

# Perspective API for toxicity / content moderation
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
# Set environment variable PERSPECTIVE_API_KEY
API_KEY = os.getenv("PERSPECTIVE_API_KEY")

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}


def moderate_vendor_notes(vendor_text: str) -> bool:
    """Return True if the vendor note is safe, False if flagged for review."""
    payload = {
        "comment": {"text": vendor_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(PERSPECTIVE_API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    # Threshold can be tuned; 0.8 is a typical conservative value
    return score < 0.8


# Example usage (not executed in this generation)
# print(moderate_vendor_notes("Some suspicious claim..."))
