import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError

def check_unsafe_content(text_payload: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Google Cloud Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        cache_discovery=False
    )

    analyze_request = {
        'comment': {'text': text_payload},
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
        return response
    except HttpError as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

