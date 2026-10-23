from security_client import get_perspective_api_client

def check_content_safety(text_payload: str, threshold=0.7):
    """
    Analyzes a text payload for toxicity using the Google Perspective API.
    """
    client = get_perspective_api_client()

    analyze_request = {
        'comment': {'text': text_payload},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

        is_safe = toxicity_score < threshold
        return {
            "is_safe": is_safe,
            "toxicity_score": toxicity_score,
            "threshold": threshold
        }
    except Exception as e:
        return {
            "error": str(e),
            "is_safe": False # Fail closed
        }
