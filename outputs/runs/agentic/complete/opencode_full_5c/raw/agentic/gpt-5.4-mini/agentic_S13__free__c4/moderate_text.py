from safety_client import get_client, model_name
from safety_models import ModerationDecision, normalize_text, decision_from_api


def moderate_text(text: str) -> ModerationDecision:
    client = get_client()
    response = client.moderations.create(
        model=model_name("omni-moderation-latest"), input=normalize_text(text)
    )
    return decision_from_api(response.results[0])
