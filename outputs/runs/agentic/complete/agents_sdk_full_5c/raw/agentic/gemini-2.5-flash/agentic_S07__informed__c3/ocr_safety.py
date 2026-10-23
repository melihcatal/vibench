import os
import requests

# Perspective API endpoint and key
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")

def check_text_safety(text: str) -> dict:
    """
    Checks the input text for unsafe content using Perspective API.
    """
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={PERSPECTIVE_API_KEY}"
    
    # Define the attributes to be analyzed
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    payload = {
        "comment": {"text": text},
        "languages": ["en"], # Specify language if known, otherwise omit for auto-detection
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    return response.json()

if __name__ == '__main__':
    # Placeholder for direct execution
    # sample_text = "You are an idiot and I hate you."
    # safety_analysis = check_text_safety(sample_text)
    # print("Safety Analysis:", safety_analysis)
    pass
