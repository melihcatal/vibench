import os
import requests
import json

def check_unsafe_content(localized_copy: str) -> dict:
    """Checks localized copy for unsafe content using the Perspective API.

    The Perspective API is a tool that uses machine learning to identify toxic comments
    and other harmful content to help improve online conversations.

    Args:
        localized_copy: The translated text to check for unsafe content.

    Returns:
        A dictionary summarizing the scores for various unsafe content attributes.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable not set. "
            "Please set it to your Perspective API key."
        )

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # The attributes to analyze for unsafe content
    # A comprehensive list can be found in the Perspective API documentation.
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": localized_copy},
        "languages": ["en"], # Perspective API works best when language is specified. Assuming English for analysis.
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        analysis_results = response.json()
        
        summary = {"scores": {}, "message": ""
        }

        for attribute, details in analysis_results.get("attributeScores", {}).items():
            summary["scores"][attribute] = details["summaryScore"]["value"]
        
        summary["message"] = (
            "Scores closer to 1 indicate higher likelihood of the attribute. "
            "Interpret based on your application's tolerance thresholds."
        )

        return summary

    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to connect to Perspective API."}
