import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_for_unsafe_content(text: str, lang: str) -> dict:
    """
    Checks text for unsafe content using the Google Perspective API.
    
    This function requires the PERSPECTIVE_API_KEY environment variable.
    The 'lang' parameter should be an ISO 639-1 language code.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Provider-specific client class and API service name ('commentanalyzer')
    # The client connects to the Perspective API hostname implicitly.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text, 'type': 'PLAIN_TEXT'},
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

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {attr: resp['summaryScore']['value'] for attr, resp in response['attributeScores'].items()}
        return scores
    except HttpError as e:
        print(f"Perspective API error: {e}")
        return {"error": str(e)}
