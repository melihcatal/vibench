import os
import deepl
from observability_models import TranslationRequest


def dashboard_note_translate(request: TranslationRequest) -> dict:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)

        result = translator.translate_text(
            request.text, target_lang=request.target_language
        )

        return {
            "original_text": request.text,
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "target_language": request.target_language,
        }
    except deepl.DeepLException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
