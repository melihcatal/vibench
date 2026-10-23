import requests
import os
from typing import List, Dict, Any

# Perspective API endpoints and attributes
_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
_DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION"
]

def check_text_safety_perspective(text: str, attributes: List[str] = _DEFAULT_ATTRIBUTES) -> Dict[str, float]:
    """Checks text content for safety using the Perspective API.

    Args:
        text: The text string to analyze.
        attributes: A list of attributes to request scores for.

    Returns:
        A dictionary where keys are attribute names and values are their scores (0-1).
        Returns an empty dict if API key is missing or an error occurs.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        print("PERSPECTIVE_API_KEY environment variable not set. Cannot perform text safety check.")
        return {}

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {attr: {} for attr in attributes},
        'languages': ['en'] # Specify language, Perspective API supports multiple
    }

    try:
        response = requests.post(
            f"{_API_BASE_URL}?key={api_key}",
            json=analyze_request
        )
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        scores = {}
        for attr in attributes:
            attribute_score = result.get('attributeScores', {}).get(attr, {})
            summary_score = attribute_score.get('summaryScore', {})
            scores[attr] = summary_score.get('value', 0.0)
        return scores

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {}

if __name__ == '__main__':
    print("Running visual_safety_text.py example...")
    sample_labels = ["gun", "knife", "happy dog", "a political rally", "violence"] # Example labels
    text_to_check = ", ".join(sample_labels)

    # Set PERSPECTIVE_API_KEY environment variable
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    if os.environ.get("PERSPECTIVE_API_KEY"):
        print(f"Checking text: '{text_to_check}'")
        safety_scores = check_text_safety_perspective(text_to_check)
        if safety_scores:
            print("Perspective API Safety Scores:")
            for attribute, score in safety_scores.items():
                print(f"  {attribute}: {score:.4f}")
        else:
            print("Could not retrieve safety scores.")
    else:
        print("Please set the PERSPECTIVE_API_KEY environment variable to run this example.")
