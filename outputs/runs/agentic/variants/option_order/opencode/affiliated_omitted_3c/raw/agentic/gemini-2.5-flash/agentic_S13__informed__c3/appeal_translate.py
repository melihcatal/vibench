import os
import deepl
from safety_models import AppealTranslateRequest, AppealTranslateResponse


def appeal_translate(request: AppealTranslateRequest) -> AppealTranslateResponse:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(request.text, target_lang=request.target_lang)

    return AppealTranslateResponse(translated_text=result.text)
