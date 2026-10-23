from openai import OpenAI

from safety_client import get_openai_client, get_moderation_model
from safety_models import normalize_moderation_result


client: OpenAI = get_openai_client()
MODEL_ID = get_moderation_model()


def moderate_text(text: str) -> dict:
    response = client.moderations.create(model=MODEL_ID, input=text)
    result = response.results[0]
    return normalize_moderation_result(result)
