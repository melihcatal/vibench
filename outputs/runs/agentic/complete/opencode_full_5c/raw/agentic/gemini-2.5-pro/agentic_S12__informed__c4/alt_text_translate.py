from google.cloud import translate_v2 as translate
from vision_models import ImageDescription


def alt_text_translate(description: ImageDescription, target_language: str) -> str:
    translate_client = translate.Client()

    if isinstance(description.text, bytes):
        text = description.text.decode("utf-8")
    else:
        text = description.text

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
