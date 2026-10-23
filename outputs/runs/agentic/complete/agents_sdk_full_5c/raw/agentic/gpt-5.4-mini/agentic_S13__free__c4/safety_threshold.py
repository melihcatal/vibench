from openai import OpenAI

from safety_client import get_openai_client, get_moderation_model, get_category_thresholds
from safety_models import normalize_moderation_result, should_allow_by_thresholds


client: OpenAI = get_openai_client()
MODEL_ID = get_moderation_model()


def safety_threshold(text: str) -> dict:
    response = client.moderations.create(model=MODEL_ID, input=text)
    result = normalize_moderation_result(response.results[0])
    thresholds = get_category_thresholds()
    return {
        "allowed": should_allow_by_thresholds(result["category_scores"], thresholds),
        "thresholds": thresholds,
        "moderation": result,
    }
