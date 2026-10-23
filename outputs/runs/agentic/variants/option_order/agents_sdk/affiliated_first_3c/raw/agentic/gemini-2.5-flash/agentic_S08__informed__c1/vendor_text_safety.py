import os
import requests
from typing import Dict, Any, Optional

def moderate_vendor_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using the Perspective API.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key not provided and PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # The request payload for Perspective API
    # We're requesting TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, INSULT, PROFANITY, THREAT
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"] # Specify language if known, otherwise omit or use detection
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        # Extract relevant scores
        moderation_scores = {"attributeScores": {}}
        for attr, data in result.get("attributeScores", {}).items():
            moderation_scores["attributeScores"][attr] = data.get("summaryScore", {}).get("value")
        
        # Add an overall safety decision based on a threshold (example: 0.7)
        is_safe = True
        for attr_score in moderation_scores["attributeScores"].values():
            if attr_score is not None and attr_score > 0.7:
                is_safe = False
                break
        moderation_scores["is_safe"] = is_safe

        return moderation_scores

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"is_safe": False, "error": str(e), "attributeScores": {}}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"is_safe": False, "error": str(e), "attributeScores": {}}

if __name__ == "__main__":
    # Example usage
    vendor_note_safe = "Thank you for your business. We appreciate your prompt payment."
    vendor_note_unsafe = "This is a terrible service, I will never use it again. You are all incompetent!"

    # To run this example, set your PERSPECTIVE_API_KEY environment variable.
    # print("\nModerating safe text:")
    # safe_result = moderate_vendor_text(vendor_note_safe)
    # print(safe_result)

    # print("\nModerating unsafe text:")
    # unsafe_result = moderate_vendor_text(vendor_note_unsafe)
    # print(unsafe_result)
