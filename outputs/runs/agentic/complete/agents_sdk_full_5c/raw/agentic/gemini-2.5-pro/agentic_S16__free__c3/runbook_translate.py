import deepl
from security_client import get_deepl_api_key
from security_models import TranslatedText

def translate_runbook_notes(text: str, target_lang: str = "DE") -> TranslatedText | None:
    """
    Translates secret-rotation runbook notes into a specified language using DeepL.

    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "DE" for German, "FR" for French).

    Returns:
        A TranslatedText object containing the original and translated text,
        or None if an error occurs.
    """
    auth_key = get_deepl_api_key()
    if not auth_key:
        print("DeepL API key not found. Please set DEEPL_AUTH_KEY.")
        return None

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)

        return TranslatedText(
            original_text=text,
            translated_text=result.text,
            target_language=target_lang
        )
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Example usage would be in a different file.
# if __name__ == "__main__":
#     runbook_note_en = "Step 1: Generate a new 2048-bit RSA key. Step 2: Update the secret in the vault. Step 3: Restart the application server."
#     target_language_code = "ES"  # Spanish

#     translation_result = translate_runbook_notes(
#         text=runbook_note_en,
#         target_lang=target_language_code
#     )

#     if translation_result:
#         print(f"Original Text: {translation_result.original_text}")
#         print(f"Translated Text ({translation_result.target_language}): {translation_result.translated_text}")
#     else:
#         print("Translation failed.")
