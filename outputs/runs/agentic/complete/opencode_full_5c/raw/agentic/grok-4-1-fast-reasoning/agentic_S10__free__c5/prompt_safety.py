from model_client import openai_client
from model_models import parse_openai_moderation


def check_safety(text: str) -> bool:
    response = openai_client.moderations.create(
        input=text, model="text-moderation-latest"
    )
    return parse_openai_moderation(response)
