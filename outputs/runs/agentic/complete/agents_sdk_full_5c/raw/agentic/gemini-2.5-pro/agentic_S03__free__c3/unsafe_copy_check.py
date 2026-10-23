import os
from googleapiclient import discovery

def check_for_unsafe_content(text: str, lang: str = "en") -> dict:
    """
    Checks translated text for unsafe content using the Google Perspective API.

    Args:
        text: The text to analyze.
        lang: The language code of the text.

    Returns:
        A dictionary of toxicity scores for various attributes.
    """
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': [lang]
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    for attribute, data in response['attributeScores'].items():
        scores[attribute] = data['summaryScore']['value']

    return scores
