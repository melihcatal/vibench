from safety_client import get_openai_client, moderation_model, text_to_messages
from safety_models import normalize_moderation_response


def moderate_text(text: str):
    client = get_openai_client()
    response = client.moderations.create(
        model=moderation_model(), input=text_to_messages(text)[0]["content"]
    )
    return normalize_moderation_response(response.model_dump())
