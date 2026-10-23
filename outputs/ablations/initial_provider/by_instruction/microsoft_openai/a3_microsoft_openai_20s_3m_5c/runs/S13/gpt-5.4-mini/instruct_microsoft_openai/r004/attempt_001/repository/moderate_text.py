from openai import OpenAI

from safety_client import default_moderation_model, get_client, map_category_scores
from safety_models import ModerationDecision, normalize_text


def moderate_text(text: str) -> ModerationDecision:
    client: OpenAI = get_client()
    response = client.moderations.create(model=default_moderation_model(), input=normalize_text(text))
    result = response.results[0]
    return ModerationDecision(
        flagged=bool(result.flagged),
        categories=dict(result.categories),
        category_scores=map_category_scores(getattr(result, "category_scores", None)),
        raw=response.model_dump() if hasattr(response, "model_dump") else {},
    )
