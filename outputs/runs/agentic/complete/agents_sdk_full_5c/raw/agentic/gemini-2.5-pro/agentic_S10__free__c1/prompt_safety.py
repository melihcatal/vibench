import os
from googleapiclient import discovery
from model_client import GOOGLE_API_KEY

def check_safety(text: str) -> dict:
    """
    Checks text for unsafe content using the Google Perspective API.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY for Perspective API not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=GOOGLE_API_KEY,
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
        }
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores
    except Exception as e:
        return {"error": str(e)}
