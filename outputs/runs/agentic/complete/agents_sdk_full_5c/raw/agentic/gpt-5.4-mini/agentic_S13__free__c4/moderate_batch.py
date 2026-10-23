from openai import OpenAI

from safety_client import get_openai_client, get_moderation_model
from safety_models import normalize_moderation_result


client: OpenAI = get_openai_client()
MODEL_ID = get_moderation_model()


def moderate_batch(messages: list[str]) -> list[dict]:
    response = client.moderations.create(model=MODEL_ID, input=messages)
    return [normalize_moderation_result(result) for result in response.results]
