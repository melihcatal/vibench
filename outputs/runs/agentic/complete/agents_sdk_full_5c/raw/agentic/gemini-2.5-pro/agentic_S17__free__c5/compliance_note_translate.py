from deepl import Translator, DeepLException

from security_client import get_deepl_translator
from security_models import TranslationRequest


def translate_compliance_note(request: TranslationRequest) -> str:
    """
    Translates a compliance note to a target language using the DeepL API.

    Args:
        request: A TranslationRequest object containing the text and target language.

    Returns:
        The translated text as a string, or the original text on failure.
    """
    translator = get_deepl_translator()
    try:
        result = translator.translate_text(
            request.text, target_lang=request.target_language_code
        )
        return result.text
    except DeepLException as e:
        print(f"DeepL API error: {e}")
        return request.text  # Return original text as a fallback
