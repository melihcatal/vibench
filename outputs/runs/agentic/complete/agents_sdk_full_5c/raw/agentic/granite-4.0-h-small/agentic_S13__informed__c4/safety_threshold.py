from typing import Dict, Optional
from safety_models import CategoryScore, NormalizedScore
from safety_client import SizeLimitedJSONEncoder

# Use a generic provider: OpenAI moderation thresholds
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = 'https://api.openai.com/v1/moderations'

def apply_category_threshold(scores: Dict[str, CategoryScore],
                             thresholds: Dict[str, float] = None) -> Dict[str, Optional[NormalizedScore]]:
    """Applies thresholds to decide whether each moderation category passes.

    Returns a dict mapping category -> NormalizedScore (True/False) or None if category not present.
    """
    if thresholds is None:
        # Default to 0.5 for all supported categories (OpenAI flag names)
        thresholds = {
            'self_harm': 0.5,
            'hate': 0.5,
            'hate_threat': 0.5,
            'sexual': 0.5,
            'sexual_minors': 0.5,
            'violence': 0.5,
            'violence_threat': 0.5,
            'harassment': 0.5,
            'self_harm_minors': 0.5,
        }
    decisions: Dict[str, Optional[NormalizedScore]] = {}
    for category, score_info in scores.items():
        category_score = score_info.get('severity') or 0.0
        thresh = thresholds.get(category, 0.5)
        decisions[category] = (category_score <= thresh, category_score)
    return decisions
