import requests
from safety_client import get_hive_api_key
from safety_models import ModerationRequest, ThresholdDecision

# Define thresholds for different categories (0.0 to 1.0)
# A higher value means a stricter policy.
THRESHOLDS = {
    "hate": 0.8,
    "violence": 0.7,
    "sexual_content": 0.6,
    "spam": 0.9,
}

def apply_safety_threshold(request: ModerationRequest) -> ThresholdDecision:
    """
    Applies predefined category thresholds to decide whether to allow text,
    using Hive Moderation for scoring.

    Args:
        request: A ModerationRequest object.

    Returns:
        A ThresholdDecision object indicating if the text is allowed.
    """
    api_key = get_hive_api_key()
    api_url = "https://api.thehive.ai/api/v2/task/sync"
    
    payload = {
        "text": request.text,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"token {api_key}"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    
    api_result = response.json()
    
    # Hive returns a list of status objects, one for each model run.
    # We find the 'text_classification' output.
    scores = {}
    for status in api_result.get('status', []):
        if status.get('response') and status['response'].get('output'):
            for output in status['response']['output']:
                if output.get('name') == 'text_classification':
                    for cls in output['classes']:
                        scores[cls['class']] = cls['score']

    if not scores:
        return ThresholdDecision(allow=True, reason="No scores returned from API.", scores={})

    for category, threshold in THRESHOLDS.items():
        if scores.get(category, 0.0) > threshold:
            return ThresholdDecision(
                allow=False,
                reason=f"Exceeded threshold for '{category}'.",
                scores=scores
            )
            
    return ThresholdDecision(allow=True, reason="All categories within threshold.", scores=scores)
