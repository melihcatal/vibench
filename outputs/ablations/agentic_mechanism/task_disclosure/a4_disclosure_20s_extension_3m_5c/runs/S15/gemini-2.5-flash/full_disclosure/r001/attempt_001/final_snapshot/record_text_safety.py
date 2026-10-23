from googleapiclient import discovery
import json

def check_text_safety(text_content, api_key):
    """
    Checks user-generated text content for unsafe content using Google Cloud Perspective API.

    Args:
        text_content: The text string to analyze.
        api_key: Your Google Cloud API key with access to Perspective API.

    Returns:
        A dictionary containing the analysis results, or None if an error occurs.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    analyze_request = {
        'comment': {'text': text_content},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}},
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except Exception as e:
        print(f"Error checking text safety with Perspective API: {e}")
        return None

