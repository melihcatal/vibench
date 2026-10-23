from typing import Dict, Optional
from embeddings_client import get_perspective_client

def check_text_safety(text: str) -> Optional[Dict]:
    """
    Checks corpus text for toxicity before embedding using Google's Perspective API.

    Args:
        text: The text to analyze.

    Returns:
        A dictionary with the toxicity score, or None on error.
    """
    try:
        perspective_client = get_perspective_client()

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en']
        }

        response = perspective_client.comments().analyze(body=analyze_request).execute()
        
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        
        return {"toxicity_score": toxicity_score}
    except Exception:
        # In a real application, log the error
        return None
