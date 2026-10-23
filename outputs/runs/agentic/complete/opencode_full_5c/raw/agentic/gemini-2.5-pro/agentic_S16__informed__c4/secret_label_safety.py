import os
import requests


def check_text_safety(text_content: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text_content},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "PROFANITY": {},
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {}


if __name__ == "__main__":
    unsafe_label = "this is a really stupid and horrible label"
    safe_note = "Standard production API key for data ingestion service."

    print(f"--- Checking unsafe text: '{unsafe_label}' ---")
    unsafe_result = check_text_safety(unsafe_label)
    if unsafe_result:
        toxicity_score = (
            unsafe_result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )
        print(f"Toxicity score: {toxicity_score}")

    print(f"\n--- Checking safe text: '{safe_note}' ---")
    safe_result = check_text_safety(safe_note)
    if safe_result:
        toxicity_score = (
            safe_result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )
        print(f"Toxicity score: {toxicity_score}")
