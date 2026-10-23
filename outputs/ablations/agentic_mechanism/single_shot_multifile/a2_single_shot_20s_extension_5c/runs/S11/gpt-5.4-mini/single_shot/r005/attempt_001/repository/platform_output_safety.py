from openai import OpenAI
from model_client import get_platform_client
from model_models import normalize_text_response


def platform_output_safety(text: str) -> bool:
    client = get_platform_client()
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    result = moderation.results[0]
    return not bool(getattr(result, "flagged", False))
