from safety_client import get_content_safety_client
from safety_models import get_text_moderation_options, parse_moderation_result

def moderate_text(text: str) -> dict:
    client = get_content_safety_client()
    options = get_text_moderation_options()
    response = client.analyze_text(options, text=text)
    scores = parse_moderation_result(response)
    scores['blocked'] = getattr(response, 'blocked', False)
    return scores
