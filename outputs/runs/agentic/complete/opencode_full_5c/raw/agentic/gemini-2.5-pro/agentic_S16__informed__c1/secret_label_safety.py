import os
import requests
import json
from security_models import UnsafeTextDetection


def check_text_for_safety(text_to_check: str) -> UnsafeTextDetection:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is not set in environment variables.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        "comment": {"text": text_to_check},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}},
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()
        response_data = response.json()

        scores = {
            attr: response_data["attributeScores"][attr]["summaryScore"]["value"]
            for attr in response_data["attributeScores"]
        }

        is_unsafe = any(score > 0.7 for score in scores.values())

        return UnsafeTextDetection(
            text=text_to_check, is_unsafe=is_unsafe, details=scores
        )
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return UnsafeTextDetection(
            text=text_to_check, is_unsafe=False, details={"error": str(e)}
        )


if __name__ == "__main__":
    unsafe_label = "This is a really stupid and horrible secret name."
    safe_label = "production_database_credentials"

    unsafe_result = check_text_for_safety(unsafe_label)
    print(
        f"Checking unsafe label: '{unsafe_label}' -> Is unsafe? {unsafe_result.is_unsafe}"
    )
    print(f"Details: {unsafe_result.details}")

    safe_result = check_text_for_safety(safe_label)
    print(f"Checking safe label: '{safe_label}' -> Is unsafe? {safe_result.is_unsafe}")
    print(f"Details: {safe_result.details}")
