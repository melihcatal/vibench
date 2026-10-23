import os
import deepl
from speech_models import TranslationRequest

def translate_text_deepl(request: TranslationRequest) -> str:
    """
    Translates text using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    # Free API does not support target_lang as 'en' but 'en-US' or 'en-GB'
    # Check for target_lang in "en" and adjust if necessary for DeepL
    if request.target_lang == "en":
        target_lang_deepl = "en-US" # Or "en-GB"
    else:
        target_lang_deepl = request.target_lang

    result = translator.translate_text(
        request.text,
        target_lang=target_lang_deepl
    )
    return result.text

if __name__ == "__main__":
    # Example usage
    sample_text = "Hallo Welt! Wie geht es dir heute?"
    target_language = "en" # DeepL often requires more specific codes like 'en-US' or 'en-GB'

    if not os.getenv("DEEPL_AUTH_KEY"):
        print("Please set the DEEPL_AUTH_KEY environment variable.")
    else:
        translation_request = TranslationRequest(text=sample_text, target_lang=target_language)
        try:
            translated_text = translate_text_deepl(translation_request)
            print(f"Original: {sample_text}")
            print(f"Translated to {target_language}: {translated_text}")
        except Exception as e:
            print(f"An error occurred: {e}")
