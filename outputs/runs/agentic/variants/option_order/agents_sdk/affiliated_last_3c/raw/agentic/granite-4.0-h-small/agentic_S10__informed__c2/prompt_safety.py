import os
import requests

# Perspective API key from env
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": PERSPECTIVE_API_KEY,
}

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

UNSAFE_SCORE_THRESHOLD = 0.7

def is_unsafe(text: str) -> bool:
    """Checks the text against Perspective API for toxicity.

    Returns True if flagged as unsafe, False otherwise.
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(PERSPECTIVE_URL, json=payload, headers=HEADERS)
    resp.raise_for_status()
    attrs = resp.json()["attributeScores"]["TOXICITY"]
    summary = attrs.get("summaryOfScores", {})
    score = summary.get("value", 0.0)
    return score >= UNSAFE_SCORE_THRESHOLD


def sanitize_prompt(prompt: str) -> str:
    """Removes or masks unsafe fragments.

    This example simply returns an empty string if unsafe; a real
    pipeline could replace offensive words with placeholders.
    """
    if is_unsafe(prompt):
        return "[Content blocked: unsafe text detected]"
    return prompt

# Example usage (can be dropped in actual code)
# if __name__ == "__main__":
#     print(sanitize_prompt("Some hateful rant"))
