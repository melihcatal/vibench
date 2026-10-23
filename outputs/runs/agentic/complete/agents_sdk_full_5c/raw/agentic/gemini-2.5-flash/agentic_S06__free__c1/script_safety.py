import os
from googleapiclient import discovery

def check_script_safety(text: str, api_key: str) -> dict:
    """Checks narration scripts for unsafe content using the Perspective API.

    Args:
        text: The script content to check.
        api_key: Your Perspective API key.

    Returns:
        A dictionary containing safety scores.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
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
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {}
    if 'attributeScores' in response:
        for attribute, value in response['attributeScores'].items():
            if 'summaryScore' in value and 'value' in value['summaryScore']:
                scores[attribute] = value['summaryScore']['value']
    return scores
