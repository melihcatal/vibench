import os
from googleapiclient import discovery
from model_models import SafetyAssessment

def check_text_safety(text: str) -> SafetyAssessment:
    """
    Checks text for harmful content using the Google Perspective API.
    
    Requires a PERSPECTIVE_API_KEY environment variable.
    Note: You must enable the 'Comment Analyzer API' in your Google Cloud project.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-specific client: googleapiclient.discovery
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
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    scores = {
        attr: response['attributeScores'][attr]['summaryScore']['value']
        for attr in response['attributeScores']
    }
    
    return SafetyAssessment(scores)
