from google.cloud import translate_v2 as translate
from vision_models import Translation

def alt_text_translate(alt_text: str, target_language: str = "es") -> Translation:
    client = translate.Client()
    result = client.translate(alt_text, target_language=target_language)
    return Translation(
        original=alt_text,
        translated=result["translatedText"],
        target_lang=target_language
    )