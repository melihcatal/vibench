import requests
from security_models import SecretPayloadModel

# Example using Perspective API for toxicity detection
PERSPECTIVE_API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
# Assumes environment variable PERSPECTIVE_API_KEY is set

def is_secret_label_safe(payload: dict, threshold: float = 0.5) -> bool:
    """Check secret payload labels/notes for unsafe content using Perspective API.

    The function sends the 'description' field (or any 'note' field) to the API
    and returns False if the toxicity score exceeds the threshold.

    Args:
        payload (dict): Secret payload, expected to contain a 'description' key.
        threshold (float): Toxicity score above which the content is considered unsafe.

    Returns:
        bool: True if safe, False otherwise.
    """
    text = payload.get('description', '')
    if not text:
        # If no description, assume safe
        return True
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={'key': os.getenv('PERSPECTIVE_API_KEY')},
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
    )
    result = response.json()
    score = result['attributeScores']['TOXICITY']['summaryScore']['value']
    return score <= threshold
