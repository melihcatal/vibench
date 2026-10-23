from document_models import ContentModerationResult
from document_client import get_perspective_api_client # Concrete provider: Google Cloud Perspective API
import requests

def moderate_text(text_content: str) -> ContentModerationResult:
    client_config = get_perspective_api_client()
    api_key = client_config["api_key"]
    api_endpoint = client_config["api_endpoint"]

    # The categories of analysis to perform. Customize as needed.
    requested_attributes = {
        'TOXICITY': {},
        'SEVERE_TOXICITY': {},
        'IDENTITY_ATTACK': {},
        'INSULT': {},
        'PROFANITY': {},
        'THREAT': {},
    }

    payload = {
        'comment': {'text': text_content},
        'requestedAttributes': requested_attributes,
        'languages': ['en']
    }

    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}

    response = requests.post(api_endpoint, headers=headers, params=params, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    analysis_result = response.json()

    scores = {}
    is_safe = True
    for attribute, data in analysis_result.get('attributeScores', {}).items():
        score = data.get('summaryScore', {}).get('value', 0.0)
        scores[attribute] = score
        # Define a threshold for what is considered 'unsafe'
        if score > 0.7: # Example threshold
            is_safe = False

    return ContentModerationResult(is_safe=is_safe, scores=scores)
