from messaging_client import get_translation_client
from messaging_models import MessagePayload


def translate_text(payload: MessagePayload, target_language: str) -> str:
    client = get_translation_client()

    if isinstance(payload.text, bytes):
        text_to_translate = payload.text.decode("utf-8")
    else:
        text_to_translate = payload.text

    result = client.translate(text_to_translate, target_language=target_language)
    return result["translatedText"]
