from identity_client import google_translate_request
from identity_models import TranslateRequest, normalize_translation


def welcome_translate(
    text: str, target_locale: str, source_locale: str | None = None
) -> dict:
    request = TranslateRequest(
        text=text, target_locale=target_locale, source_locale=source_locale
    )
    payload = {
        "q": request.text,
        "target": request.target_locale,
        "format": "text",
    }
    if request.source_locale:
        payload["source"] = request.source_locale
    response = google_translate_request(payload)
    normalized = normalize_translation(response)
    normalized["target_locale"] = target_locale
    return normalized
