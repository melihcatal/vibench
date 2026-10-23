import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable for content safety checks.")

HEADERS = {
    "Content-Type": "application/json",
    "x-goog-api-key": PERSPECTIVE_API_KEY,
}


def check_unsafe(text: str, target_languages: list[str] = None) -> bool:
    """Return True if the content is flagged as unsafe.",
    Args:
        text (str): Narration script.
        target_languages (list[str]): ISO language codes to request additional models.",
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    if target_languages:
        payload["languages"] += target_languages
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=HEADERS)
    result = response.json()
    attrs = result.get("attributeScores", {})
    unsafe = (
        attrs.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0) >= 0.8
        or attrs.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0) >= 0.8
    )
    return unsafe

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     unsafe = check_unsafe("This is a nasty comment!")
#     print("Unsafe?", unsafe)
