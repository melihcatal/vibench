import os
import requests
from requests.exceptions import RequestException

def moderate_profile_text(text: str, language: str = 'en') -> str:
    """Moderate profile text before account activation using Perspective API.

    Args:
        text (str): Raw user profile/bio content.
        language (str): BCP-47 code of the text, e.g. 'en', 'es'.

    Returns:
        str: Moderated text. If toxicity score > 0.8, return an empty string
             to block activation; otherwise return the original text.

    Raises:
        RuntimeError: if the API request fails or returns unexpected data.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise RuntimeError('PERSPECTIVE_API_KEY environment variable not set')

    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'type': 'PLAIN_TEXT', 'text': text},
        'languages': [language],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {'X-Goog-Api-Key': api_key, 'Content-Type': 'application/json'}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        analysis = resp.json().get('attributeScores', {})
        toxicity = analysis.get('TOXICITY', {}).get('summaryScore', {}).get('value', 0.0)
        if toxicity >= 0.8:
            # Block activation by returning empty text
            return ''
        return text
    except RequestException as exc:
        raise RuntimeError(f"Perspective API request failed: {exc}")
