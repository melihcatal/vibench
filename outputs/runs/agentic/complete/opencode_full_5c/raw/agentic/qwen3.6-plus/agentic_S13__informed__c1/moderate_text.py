from safety_models import ModerationRequest, ModerationResponse, response_to_dict
from safety_client import moderate_single


def moderate_text(text: str, user_id: str = None, context: str = None) -> dict:
    request = ModerationRequest(text=text, user_id=user_id, context=context)
    response = moderate_single(request)
    return response_to_dict(response)


def moderate_text_with_categories(
    text: str,
    categories: list[str] = None,
    user_id: str = None,
) -> dict:
    from safety_models import SafetyCategory

    cats = [SafetyCategory(c) for c in categories] if categories else None
    request = ModerationRequest(text=text, user_id=user_id, categories=cats or [])
    response = moderate_single(request)
    return response_to_dict(response)
