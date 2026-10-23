import os
import requests
from typing import Dict, Any

def check_text_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using the Perspective API.
    Requires PERSPECTIVE_API_KEY to be set in the environment.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The base URL for the Perspective API
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        'comment': {'text': text_content},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en'] # Specify language, adjust as needed
    }

    response = requests.post(url, json=request_body)
    response.raise_for_status() # Raise an exception for HTTP errors
    
    return response.json()

if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY env var)
    sample_text = "You are an idiot and I hate you!"
    # safety_report = check_text_safety(sample_text)
    # print(f"Safety Report: {safety_report}")
    print("To run this example, ensure PERSPECTIVE_API_KEY is set and uncomment the example usage.")
