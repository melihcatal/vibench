
from googleapiclient import discovery
import json

def check_unsafe_text(text_content: str) -> dict:
    """
    Checks the given text content for unsafe attributes using Google Cloud's Perspective API.

    Args:
        text_content: The text string to be analyzed.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey="YOUR_API_KEY" # Replace with your actual API key or environment variable
    )

    analyze_request = {
        'comment': {'text': text_content},
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
    return response

