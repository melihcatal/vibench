import os
from googleapiclient import discovery

def check_text_safety(text: str) -> dict:
    """
    Checks user-generated text for unsafe content using Google's Perspective API.

    :param text: The text to analyze.
    :return: A dictionary with toxicity scores.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores
    except Exception as e:
        print(f"Perspective API call failed: {e}")
        return {"error": "Failed to analyze text"}
