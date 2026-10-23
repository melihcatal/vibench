from security_client import get_deepl_translator
from security_models import TranslationPayload


def translate_compliance_note(payload: TranslationPayload) -> str:
    translator = get_deepl_translator()

    try:
        result = translator.translate_text(
            payload.text, target_lang=payload.target_lang
        )
        return result.text
    except Exception as e:
        return f"Translation failed: {e}"
