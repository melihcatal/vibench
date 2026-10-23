import os
import requests
from security_models import SafetyCheckRequest, SafetyCheckResponse


def check_payload_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Checks decrypted text payloads for unsafe content using the Perspective API.

    Args:
        request: A SafetyCheckRequest object containing the text payload to check.

    Returns:
        A SafetyCheckResponse object indicating if the payload is safe and reasons if not.
    """
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + perspective_api_key
    )

    # The request body for Perspective API
    analyze_request = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            # Add other attributes as needed
        },
    }

    try:
        response = requests.post(api_url, json=analyze_request)
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_results = response.json()

        is_safe = True
        reasons = []

        # Define a threshold for what's considered unsafe (e.g., 0.7 for any attribute)
        THRESHOLD = 0.7

        for attribute, scores in analysis_results.get("attributeScores", {}).items():
            summary_score = scores.get("summaryScore", {}).get("value", 0.0)
            if summary_score > THRESHOLD:
                is_safe = False
                reasons.append(
                    f"{attribute}: {summary_score:.2f} (above threshold {THRESHOLD})"
                )

        return SafetyCheckResponse(is_safe=is_safe, reasons=reasons)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error communicating with Perspective API: {e}")
    except Exception as e:
        raise RuntimeError(f"Error checking payload safety with Perspective API: {e}")
