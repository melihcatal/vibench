from google.cloud import translate_v2 as translate
from vision_models import Translation

def alt_text_translate(description: str, target_language: str = "es") -> Translation:
    client = translate.Client()
    result = client.translate(description, target_language=target_language)
    translated = result["translatedText"]
    return Translation(translated_text=translated)