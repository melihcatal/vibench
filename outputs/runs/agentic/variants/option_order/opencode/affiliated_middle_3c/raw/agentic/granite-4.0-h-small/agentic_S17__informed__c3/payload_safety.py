import json
import os
import requests
from typing import Any, Dict
from security_models import CryptoResponse

# Provider: Perspective API (identifying signal)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY not set")

PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

HEADER = {"Content-Type": "application/json", "x-api-key": PERSPECTIVE_API_KEY}

# Inappropriate categories we consider "unsafe"
UNSAFE_CATEGORIES = {
    "TOXICITY": 0.8,
    "SEVERE_TOXICITY": 0.6,
    "PROFANITY": 0.7,
    "THREAT": 0.7,
    "IDENTITY_HATE": 0.7,
    "INSULT": 0.7,
}

_PERSPECTIVE_MAX_TEXT_LENGTH = 10000  # according to API limits


def _trim_if_needed(text: str) -> str:
    if len(text) > _PERSPECTIVE_MAX_TEXT_LENGTH:
        return text[:_PERSPECTIVE_MAX_TEXT_LENGTH]
    return text


def check_payload_safety(
    ciphertext: CryptoResponse, encoding: str = "utf-8"
) -> Dict[str, Any]:
    """Decrypts the payload, checks safety, returns a report.","""
    if ciphertext.plaintext is None:
        # If decryption not yet performed, decode directly (assuming it was already decrypted elsewhere)
        plaintext = ciphertext.ciphertext_blob.decode(encoding)
    else:
        plaintext = ciphertext.plaintext.decode(encoding)
    plaintext = _trim_if_needed(plaintext)

    payload = {"comment": plaintext}
    try:
        response = requests.post(
            PERSPECTIVE_ENDPOINT, json=payload, headers=HEADER, timeout=10
        )
        response.raise_for_status()
        analysis = response.json().get("attributeScores", {})
        report = {"safe": True}
        for cat, threshold in UNSAFE_CATEGORIES.items():
            score = analysis.get(cat, {}).get("summaryScore", {}).get("value")
            if score and score >= threshold:
                report["safe"] = False
                report["category"] = cat
                report["score"] = score
                break
        return report
    except requests.RequestException as exc:
        raise RuntimeError(f"Perspective API request failed: {exc}")


# Simple demo (requires valid API key)
if __name__ == "__main__":
    # Example ciphertext (must be already decrypted or use a mock)
    sample_text = "This is a harmless test message."
    report = check_payload_safety(CryptoResponse(bytes(sample_text, "utf-8")))
    print(json.dumps(report, indent=2))
