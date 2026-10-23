from translation_client import load_config, post_translate
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    req = TranslationRequest(text=normalize_text(text), source_lang=source_lang, target_lang=target_lang)
    cfg = load_config()
    payload = {"text": [req.text], "source_lang": req.source_lang, "target_lang": req.target_lang}
    data = post_translate(payload, cfg)
    translated = data["translations"][0]["text"]
    return TranslationResponse(translated_text=translated, provider_payload=data)
