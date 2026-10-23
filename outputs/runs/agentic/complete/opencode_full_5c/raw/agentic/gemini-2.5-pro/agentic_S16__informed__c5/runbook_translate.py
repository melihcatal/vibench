import os
import deepl
from security_models import TranslationResult


def translate_text_with_deepl(text: str, target_lang: str) -> TranslationResult:
    """
    Translates runbook notes or other text using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return TranslationResult(
            source_text=text,
            translated_text=result.text,
            target_language=target_lang,
        )
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return TranslationResult(
            source_text=text, translated_text="", target_language=target_lang
        )


if __name__ == "__main__":
    runbook_notes = "Rotation failed due to database connection timeout. Manual intervention required."
    target_language = "DE"  # German
    translation = translate_text_with_deepl(runbook_notes, target_language)
    if translation.translated_text:
        print(f"Original: {translation.source_text}")
        print(
            f"Translated ({translation.target_language}): {translation.translated_text}"
        )
    else:
        print("Translation failed.")
