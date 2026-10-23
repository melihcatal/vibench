from safety_client import get_client, model_name
from safety_models import ModerationBatchResult, normalize_messages, decision_from_api


def moderate_batch(messages):
    client = get_client()
    response = client.moderations.create(
        model=model_name("omni-moderation-latest"), input=normalize_messages(messages)
    )
    return ModerationBatchResult(
        decisions=[decision_from_api(item) for item in response.results]
    )
