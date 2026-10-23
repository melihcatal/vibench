# [LATER-STEP] appeal_translate.py
# Translate appeal text for review

from google.cloud import translate_v2 as translate

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set locally
translate_client = translate.Client()


def translate_appeal(text: str, target_lang: str = "en") -> str:
    """Translate appeal text to the target language for reviewer consumption."""
    result = translate_client.translate(text, target_language=target_lang)
    return result["translatedText"]
