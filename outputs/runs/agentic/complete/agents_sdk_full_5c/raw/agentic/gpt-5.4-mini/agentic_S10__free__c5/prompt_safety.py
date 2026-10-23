from openai import OpenAI

from model_client import get_client, select_safety_model
from model_models import ModerationResult, normalize_moderation_response


PROVIDER = "openai"
DEFAULT_MODEL = "omni-moderation-latest"


def prompt_safety(text: str) -> ModerationResult:
    client = get_client()
    model = select_safety_model(default=DEFAULT_MODEL)
    resp = client.moderations.create(model=model, input=text)
    return normalize_moderation_response(resp)
