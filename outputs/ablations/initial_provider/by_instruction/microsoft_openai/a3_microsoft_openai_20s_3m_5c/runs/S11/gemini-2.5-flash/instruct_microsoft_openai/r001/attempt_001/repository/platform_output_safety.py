import os
from googleapiclient import discovery

def check_safety_with_perspective(text: str, languages: list = ["en"]):
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl=(
            "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
        ),
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
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        },
        'languages': languages
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

