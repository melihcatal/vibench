from __future__ import annotations

from identity_client import get_deepl_headers, post_json
from identity_models import WelcomeTranslateRequest


DEEPL_TRANSLATE_URL = "https://api.deepl.com/v2/translate"


def welcome_translate(request: WelcomeTranslateRequest):
    payload = {
        "text": [request.text],
        "target_lang": request.target_locale.upper().replace("-", "_").split("_")[0],
    }
    if request.source_locale:
        payload["source_lang"] = request.source_locale.upper().replace("-", "_").split("_")[0]
    response = post_json(DEEPL_TRANSLATE_URL, get_deepl_headers(), payload)
    translation = response["translations"][0]
    return {
        "translated_text": translation["text"],
        "detected_source_language": translation.get("detected_source_language"),
        "provider": "deepl",
    }
