import os
import requests

def apply_category_thresholds(text: str, thresholds: dict) -> dict:
    """Applies category thresholds to decide whether to allow text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")

    params = {"key": api_key}
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
        "doNotStore": True
    }

    try:
        response = requests.post(api_url, params=params, json=payload)
        response.raise_for_status()
        analysis_result = response.json()

        decision = {"allow_text": True, "reasons": []}
        for attribute, score_info in analysis_result.get("attributeScores", {}).items():
            score = score_info["summaryScore"]["value"]
            if attribute in thresholds and score >= thresholds[attribute]:
                decision["allow_text"] = False
                decision["reasons"].append(f"{attribute} score ({score:.2f}) exceeded threshold ({thresholds[attribute]:.2f})")
        
        decision["analysis_result"] = analysis_result
        return decision
    except requests.exceptions.RequestException as e:
        print(f"Error applying thresholds with Perspective API: {e}")
        raise
