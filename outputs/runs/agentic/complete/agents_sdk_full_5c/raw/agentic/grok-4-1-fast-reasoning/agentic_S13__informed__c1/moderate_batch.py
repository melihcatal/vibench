from typing import List, Dict
from safety_client import get_content_safety_client
from safety_models import get_text_moderation_options, parse_moderation_result

def moderate_batch(texts: List[str]) -> List[Dict]:
    client = get_content_safety_client()
    options = get_text_moderation_options()
    results = []
    for text in texts:
        response = client.analyze_text(options, text=text)
        scores = parse_moderation_result(response)
        scores['blocked'] = getattr(response, 'blocked', False)
        results.append(scores)
    return results
