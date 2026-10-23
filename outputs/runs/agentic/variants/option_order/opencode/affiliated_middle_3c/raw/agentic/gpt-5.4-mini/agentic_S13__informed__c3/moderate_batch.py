from safety_client import SafetyClient
from safety_models import BatchModerationRequest


def moderate_batch(messages: list[str], language: str | None = None):
    return SafetyClient().moderate_batch(BatchModerationRequest(messages=messages, language=language))
