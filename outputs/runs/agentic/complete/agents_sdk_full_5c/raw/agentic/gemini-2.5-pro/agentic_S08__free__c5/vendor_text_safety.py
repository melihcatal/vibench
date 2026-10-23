# vendor_text_safety.py
from document_client import get_perspective_client

def check_vendor_text_safety(text_to_analyze: str) -> dict:
    """
    Analyzes text for toxicity and other attributes using Google's Perspective API.
    """
    client = get_perspective_client()

    analyze_request = {
        'comment': {'text': text_to_analyze},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response['attributeScores'].items():
        scores[attribute] = data['summaryScore']['value']

    return scores
