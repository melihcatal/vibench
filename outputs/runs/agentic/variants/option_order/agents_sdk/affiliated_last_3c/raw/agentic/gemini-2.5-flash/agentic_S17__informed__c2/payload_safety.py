import os
import requests

def check_payload_safety(text_payload: str, client_ip: str = None) -> dict:
    """
    Checks a decrypted text payload for unsafe content using the Perspective API.

    Args:
        text_payload: The text content to analyze.
        client_ip: Optional client IP address to send to the API.

    Returns:
        A dictionary containing the analysis results from Perspective API.
    """
    api_key = os.environ.get('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    request_body = {
        'comment': {'text': text_payload},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': ['en']
    }

    if client_ip:
        request_body['clientToken'] = client_ip

    response = requests.post(url, json=request_body)
    response.raise_for_status()
    return response.json()
