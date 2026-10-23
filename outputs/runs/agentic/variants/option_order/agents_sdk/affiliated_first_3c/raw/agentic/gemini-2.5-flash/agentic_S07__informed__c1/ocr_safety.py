import os
import requests
import json

def check_text_safety_perspective_api(text: str) -> dict:
    """Checks text for unsafe content using Google's Perspective API.
    Requires a PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {
            "text": text
        },
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
        "languages": ["en"] # Specify language of the text
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

if __name__ == '__main__':
    TEXT_TO_ANALYZE = "You are an idiot and should go die."

    # Set your Perspective API Key in environment variable, e.g.:
    # export PERSPECTIVE_API_KEY="YOUR_API_KEY"

    # try:
    #     safety_scores = check_text_safety_perspective_api(TEXT_TO_ANALYZE)
    #     print(f"Safety analysis for: '{TEXT_TO_ANALYZE}'")
    #     for attribute, scores in safety_scores.get("attributeScores", {}).items():
    #         print(f"  {attribute}: {scores['summaryScore']['value']}")
    # except ValueError as e:
    #     print(e)
    # except requests.exceptions.RequestException as e:
    #     print(f"API request failed: {e}")
