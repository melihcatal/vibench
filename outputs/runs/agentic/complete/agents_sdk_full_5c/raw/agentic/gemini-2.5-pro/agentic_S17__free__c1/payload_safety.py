
import os
from googleapiclient import discovery
from typing import Dict, List

def check_payload_safety_perspective(text: str) -> Dict:
    """
    Checks decrypted text for unsafe content using the Google Perspective API.
    
    Requires a Google API key with Perspective API enabled.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # A free, publically available model provided by Google's Jigsaw
    # See: https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    requested_attributes = {
        'TOXICITY': {},
        'SEVERE_TOXICITY': {},
        'IDENTITY_ATTACK': {},
        'INSULT': {},
        'PROFANITY': {},
        'THREAT': {}
    }
    
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': requested_attributes,
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        
        scores = {}
        for attribute, data in response['attributeScores'].items():
            scores[attribute] = data['summaryScore']['value']
        
        return scores
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        # Depending on policy, might fail open or closed.
        # Failing open (assuming safe) is shown here.
        return {}
