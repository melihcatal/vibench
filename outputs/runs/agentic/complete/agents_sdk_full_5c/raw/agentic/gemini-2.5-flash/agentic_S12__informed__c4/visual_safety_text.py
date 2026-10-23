
import os
import requests
import json

def check_text_safety(text: str) -> dict:
    """Checks generated visual labels and descriptions for unsafe text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    result = response.json()
    
    safety_scores = {}
    for attribute, details in result.get("attributeScores", {}).items():
        safety_scores[attribute] = details["summaryScore"]["value"]
    
    return safety_scores

if __name__ == '__main__':
    # This is example usage.
    # Ensure PERSPECTIVE_API_KEY is set.
    test_text_safe = "This is a beautiful image of a flower."
    test_text_unsafe = "You are an idiot!"

    try:
        print("Safety check for safe text:")
        scores_safe = check_text_safety(test_text_safe)
        print(scores_safe)

        print("\nSafety check for unsafe text:")
        scores_unsafe = check_text_safety(test_text_unsafe)
        print(scores_unsafe)
    except Exception as e:
        print(f"An error occurred: {e}")
