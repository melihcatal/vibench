from safety_client import get_openai_client, moderation_model
from safety_models import normalize_batch_response


def moderate_batch(messages):
    client = get_openai_client()
    response = client.moderations.create(model=moderation_model(), input=messages)
    return normalize_batch_response(response.model_dump())
