from google.cloud import translate_v2 as translate
from vision_models import ImageDescription


def alt_text_translate(alt_text: ImageDescription, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(alt_text.description, target_language=target_language)
    return result["translatedText"]
