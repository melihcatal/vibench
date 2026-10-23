from google.cloud import translate_v2 as translate
from vision_client import get_translate_client


def translate_text(text: str, target_language: str) -> str:
    client = get_translate_client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
