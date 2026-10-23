import os
import requests
import json

def check_corpus_safety(text: str) -> dict:
    """
    Checks corpus text for toxicity using the Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary containing analysis results from the Perspective API.
    """
    api_key = os.environ.get('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}'

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

    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with Perspective API: {e}")
        return {}
