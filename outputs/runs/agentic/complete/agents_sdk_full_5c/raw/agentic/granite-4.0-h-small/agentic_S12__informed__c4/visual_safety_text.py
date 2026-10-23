from typing import List, Dict

from vision_models import normalize_safety_check

# -------------------------------------------------------------------
# Re‑check generated textual outputs (labels, captions, extracted text)
# for unsafe phrasing using an external moderation service.
# -------------------------------------------------------------------

def safety_screen_texts(texts: List[str], service: str = 'perspective') -> List[Dict[str, Any]]:
    """Run the supplied text list through the chosen moderation endpoint.

    By default uses the Perspective API (REST) which returns toxicity scores.
    Returns a list of dicts in the shape:
        [{'text': original, 'score': float, 'safe': bool}, ...]
    If another provider is requested, a placeholder switch demonstrates how it could be swapped.
    """
    # -------------------------------------------------------------------
    # Perspective API example (REST)
    # -------------------------------------------------------------------
    if service.lower() == 'perspective':
        # Note: In production you would add error handling, retries, and rate‑limit awareness.
        import requests
        URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
        PARAMS = {
            'key': os.getenv('PERSPECTIVE_API_KEY'),  # expect env var set by caller
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
        responses = []
        for txt in texts:
            payload = {
                'comment': {'text': txt},
                'languages': ['en'],
                'clientId': 'my-app-id'
            }
            r = requests.post(URL, json=payload, params=PARAMS)
            r.raise_for_status()
            score = r.json()['attributeScores']['TOXICITY']['summaryScore']['value']
            responses.append({'text': txt, 'score': float(score), 'safe': score < 0.5})
        return responses
    # -------------------------------------------------------------------
    # Placeholder for other providers (AWS Comprehend, Azure Content Safety, etc.)
    # -------------------------------------------------------------------
    else:
        raise NotImplementedError(f"Safety service '{service}' not implemented")
