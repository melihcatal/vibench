import os
from googleapiclient import discovery

def check_script_for_safety(text: str, threshold: float = 0.7) -> dict:
    """
    Checks a script for unsafe content using the Google Perspective API.

    Requires the PERSPECTIVE_API_KEY environment variable.

    Args:
        text: The script text to analyze.
        threshold: The score threshold above which content is considered unsafe.

    Returns:
        A dictionary with analysis results and a safety flag.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {
        attr: response['attributeScores'][attr]['summaryScore']['value']
        for attr in response['attributeScores']
    }
    
    is_unsafe = any(score > threshold for score in scores.values())

    return {
        "is_unsafe": is_unsafe,
        "scores": scores
    }
