import os
from google.cloud import translate_v2 as translate # Google Cloud Translation API is a provider-identifying signal
from typing import Optional

from speech_models import TranslationResult

def translate_live_caption(
    text: str,
    target_language: str,
    source_language: Optional[str] = None
) -> TranslationResult:
    """
    Translates a given live caption text into another language using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return TranslationResult(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"] if "detectedSourceLanguage" in result else source_language or "unknown",
        target_language=target_language
    )

if __name__ == "__main__":
    # Example Usage
    caption_to_translate = "Hello, how are you? This is a live caption."
    target_lang = "es"
    translated_caption = translate_live_caption(caption_to_translate, target_lang)
    print(f"Original: '{caption_to_translate}'")
    print(f"Translated ({translated_caption.target_language}): '{translated_caption.translated_text}'")

    caption_to_translate_fr = "Bonjour, comment allez-vous?"
    target_lang_en = "en"
    translated_caption_en = translate_live_caption(caption_to_translate_fr, target_lang_en, source_language="fr")
    print(f"Original: '{caption_to_translate_fr}'")
    print(f"Translated ({translated_caption_en.target_language}): '{translated_caption_en.translated_text}'")
