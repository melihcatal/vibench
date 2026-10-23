import os
import requests
import json

def check_text_safety_with_perspective(text: str, api_key: str) -> Dict[str, Any]:
    """
    Checks extracted document text for unsafe content using Perspective API.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": api_key
    }
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
        }
    }

    response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Placeholder for actual usage, demonstrating the provider integration
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    text_to_check = "You are an idiot and I hate you!"

    if perspective_api_key:
        print(f"Checking text safety for '{text_to_check}' using Perspective API...")
        # safety_analysis = check_text_safety_with_perspective(text_to_check, perspective_api_key)
        # print("Safety Analysis:", json.dumps(safety_analysis, indent=2))
    else:
        print("Please set PERSPECTIVE_API_KEY environment variable.")
