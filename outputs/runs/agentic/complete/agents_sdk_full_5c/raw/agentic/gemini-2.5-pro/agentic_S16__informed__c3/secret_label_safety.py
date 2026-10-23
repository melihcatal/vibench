import os
import requests
import json
from typing import Dict, Optional

def check_text_for_unsafe_content(text: str) -> Optional[Dict]:
    """
    Analyzes a string for toxicity and other attributes using the Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing the analysis scores, or None if an error occurs.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    try:
        response = requests.post(url, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        
        response_data = response.json()
        scores = {
            attr: response_data['attributeScores'][attr]['summaryScore']['value']
            for attr in payload['requestedAttributes']
        }
        return scores

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the Perspective API: {e}")
        return None

def check_secret_labels(secret_name: str, secret_notes: str) -> bool:
    """
    Checks if a secret's name or notes contain potentially unsafe text.
    
    Args:
        secret_name: The name/label of the secret.
        secret_notes: The descriptive notes for the secret.
        
    Returns:
        True if the content is deemed safe, False otherwise.
    """
    combined_text = f"Secret Name: {secret_name}. Notes: {secret_notes}"
    scores = check_text_for_unsafe_content(combined_text)

    if scores:
        # Define a simple threshold for "unsafe"
        if scores.get('TOXICITY', 0) > 0.7 or scores.get('THREAT', 0) > 0.6:
            print(f"Unsafe content detected in secret metadata: {scores}")
            return False
    
    return True
