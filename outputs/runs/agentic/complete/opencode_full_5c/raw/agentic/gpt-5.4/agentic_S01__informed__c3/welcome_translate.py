import requests

from identity_client import deepl_auth_key, request_timeout
from identity_models import TranslateWelcomeRequest, normalize_deepl_translation


def welcome_translate(request: TranslateWelcomeRequest):
    payload = {
        "text": [request.text],
        "target_lang": request.target_locale.upper(),
    }
    if request.source_locale:
        payload["source_lang"] = request.source_locale.upper()
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {deepl_auth_key()}"},
        timeout=request_timeout(),
    )
    response.raise_for_status()
    return normalize_deepl_translation(response.json(), request.target_locale)
