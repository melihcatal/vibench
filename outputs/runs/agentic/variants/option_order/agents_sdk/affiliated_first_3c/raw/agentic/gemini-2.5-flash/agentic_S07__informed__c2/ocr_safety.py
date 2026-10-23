import requests
import os
from typing import List, Dict, Any


def check_ocr_safety(text: str) -> Dict[str, Any]:
    """Checks extracted document text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        # Add other attributes as needed
    }

    data = {
        "comment": {"text": text},
        "languages": ["en"], # Specify languages of the input text
        "requestedAttributes": requested_attributes,
    }

    response = requests.post(url, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors

    result = response.json()
    
    unsafe_categories = []
    scores = {}

    for attribute, details in result.get("attributeScores", {}).items():
        score = details["summaryScore"]["value"]
        scores[attribute.lower()] = score
        # A common threshold for toxicity is 0.7 or 0.75, adjust as needed
        if score > 0.7:
            unsafe_categories.append(attribute.lower())
            
    return {"unsafe_categories": unsafe_categories, "scores": scores}

if __name__ == '__main__':
    # Placeholder for actual usage. Ensure PERSPECTIVE_API_KEY is set.
    sample_text_safe = "This is a perfectly safe document content."
    sample_text_unsafe = "You are an idiot and I will hurt you."

    try:
        # safe_result = check_ocr_safety(sample_text_safe)
        # print(f"Safe Text Safety Check: {safe_result}")
        # unsafe_result = check_ocr_safety(sample_text_unsafe)
        # print(f"Unsafe Text Safety Check: {unsafe_result}")
        print("Run with an actual Perspective API Key.")
    except Exception as e:
        print(f"Error checking safety: {e}")
