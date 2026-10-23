import os
from safety_client import TextSafetyClient

client = TextSafetyClient(
    service='Alibaba Content Moderation',
    api_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    secret_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-shanghai')
)

def apply_thresholds(text: str, thresholds: dict) -> bool:
    """Apply category thresholds to decide whether to allow the text.
    'thresholds' is a dict like {'toxicity': 0.65, 'hate': 0.5}.
    The method calls the provider's scoring endpoint and returns True if all
    category scores are below the supplied limits, otherwise False.
    """
    scores = client.get_category_scores(text=text)
    # scores example: {'toxicity': 0.42, 'hate': 0.78}
    for cat, limit in thresholds.items():
        if cat in scores and scores[cat] > limit:
            return False
    return True

__all__ = ['apply_thresholds']
