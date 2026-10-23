# [LATER-STEP] live_caption_translate.py

from google.cloud import translate_v2 as translate

# Identify provider: Google Cloud Translation


def translate_text(text: str, target_lang: str = "es") -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]
