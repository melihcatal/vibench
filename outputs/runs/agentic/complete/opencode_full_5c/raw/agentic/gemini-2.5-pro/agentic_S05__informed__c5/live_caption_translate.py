import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

from speech_models import TranslationResponse

load_dotenv()

# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
# for Application Default Credentials (ADC) to work.


def translate_caption(text: str, target_language: str) -> TranslationResponse:
    """Translates a text string into the target language."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResponse(translated_text=result["translatedText"])


if __name__ == "__main__":
    caption_text = "Hello, this is a live caption that needs to be translated."
    target = "es"  # Spanish
    translation = translate_caption(caption_text, target)
    print(f"Original: {caption_text}")
    print(f"Translated to '{target}': {translation.translated_text}")
