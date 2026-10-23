from speech_client import build_client, get_openai_text_model
from speech_models import normalize_text


def moderate_transcript(text: str):
    client = build_client()
    response = client.moderations.create(
        model="omni-moderation-latest", input=normalize_text(text)
    )
    return response
