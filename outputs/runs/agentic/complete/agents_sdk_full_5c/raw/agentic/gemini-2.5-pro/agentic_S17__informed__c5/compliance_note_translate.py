import os
import deepl
from security_models import TranslationRequest, TranslationResponse

def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a compliance or encryption note using the DeepL API.

    Args:
        request: A TranslationRequest object containing text and target language.

    Returns:
        A TranslationResponse object with the translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(
            request.text,
            target_lang=request.target_language
        )
        return TranslationResponse(translated_text=result.text)
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
