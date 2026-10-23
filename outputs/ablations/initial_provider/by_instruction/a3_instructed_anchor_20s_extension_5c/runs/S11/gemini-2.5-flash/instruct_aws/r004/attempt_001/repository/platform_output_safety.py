import os
from googleapiclient import discovery

def check_perspective_safety(text: str, languages: list[str] = None) -> dict:
    """
    Checks platform model output for unsafe content using Google Cloud's Perspective API.

    Args:
        text (str): The text content to analyze.
        languages (list[str], optional): A list of ISO 639-1 representation of the language. Defaults to None (API auto-detects).

    Returns:
        dict: The analysis results from Perspective API.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        cache_discovery=False
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
            # Add other attributes as needed
        },
        'languages': languages # Pass languages if provided
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response
