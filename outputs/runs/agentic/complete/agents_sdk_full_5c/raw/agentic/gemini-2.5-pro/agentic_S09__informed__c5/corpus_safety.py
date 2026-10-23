import os
import requests
import json

def check_text_safety(text: str) -> dict:
    """
    Checks text for harmful content using the Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with toxicity analysis scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The Perspective API endpoint is a clear provider signal.
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
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
        response = requests.post(url, data=json.dumps(request_body))
        response.raise_for_status()
        response_data = response.json()
        
        scores = {
            attr: scores['summaryScore']['value']
            for attr, scores in response_data['attributeScores'].items()
        }
        return scores

    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {}

