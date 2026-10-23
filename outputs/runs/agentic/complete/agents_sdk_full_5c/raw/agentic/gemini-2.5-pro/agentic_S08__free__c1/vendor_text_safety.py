from googleapiclient import discovery
from document_client import get_settings

def moderate_vendor_text(text: str) -> dict:
    """
    Analyzes text for toxicity using the Google Perspective API.

    Args:
        text: The string to analyze.

    Returns:
        A dictionary containing the analysis results for requested attributes.
    """
    api_key = get_settings().PERSPECTIVE_API_KEY
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is not set.")

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

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attribute, value in response['attributeScores'].items():
            scores[attribute] = value['summaryScore']['value']
        return scores
    except Exception as e:
        # Handle API errors gracefully
        return {"error": str(e)}

