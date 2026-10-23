import os
import requests
import json

def check_annotation_safety(text: str, client_ip: str = None) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using the Perspective API.

    Args:
        text: The free-text annotation to check.
        client_ip: Optional IP address of the client making the request, for improved analysis.

    Returns:
        A dictionary containing the safety analysis results from Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_body = {
        'comment': {'text': text},
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
        request_body['spanAnnotations'] = True # This header indicates client IP is present
        request_body['clientToken'] = client_ip # Although not directly client_ip field, this is often used.

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    return response.json()

