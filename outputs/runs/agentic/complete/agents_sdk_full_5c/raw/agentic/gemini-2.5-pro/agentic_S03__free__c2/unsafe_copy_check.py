from googleapiclient import discovery
from translation_client import GOOGLE_API_KEY

def check_for_unsafe_content(text: str, lang: str = 'en') -> dict:
    """
    Checks text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.
        lang: The language of the text.

    Returns:
        A dictionary of toxicity scores.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY for Perspective API not set.")

    # Provider-identifying signal: 'commentanalyzer' service name
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=GOOGLE_API_KEY,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'languages': [lang],
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
    for attr, value in response['attributeScores'].items():
        scores[attr] = value['summaryScore']['value']

    return scores
