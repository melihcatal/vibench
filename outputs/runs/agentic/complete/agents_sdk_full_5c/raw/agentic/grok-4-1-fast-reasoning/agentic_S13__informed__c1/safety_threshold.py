from typing import Dict
from safety_client import get_content_safety_client
from safety_models import get_text_moderation_options, parse_moderation_result

def is_text_allowed(text: str, thresholds: Dict[str, float]) -> bool:
    client = get_content_safety_client()
    options = get_text_moderation_options()
    response = client.analyze_text(options, text=text)
    scores = parse_moderation_result(response)
    for category, thresh in thresholds.items():
        if scores.get(category, 0.0) >= thresh:
            return False
    return True
