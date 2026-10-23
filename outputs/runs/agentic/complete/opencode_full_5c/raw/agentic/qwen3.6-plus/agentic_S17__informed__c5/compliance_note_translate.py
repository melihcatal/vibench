import deepl
from security_models import ComplianceTranslationRequest, ComplianceTranslationResponse
from security_client import load_deepl_config


def translate_compliance_note(
    request: ComplianceTranslationRequest,
) -> ComplianceTranslationResponse:
    config = load_deepl_config()

    auth_key = config["auth_key"]
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")

    translator = deepl.Translator(auth_key)

    target_lang = request.target_language.upper()
    source_lang = request.source_language.upper() if request.source_language else None

    translate_kwargs = {
        "target_lang": target_lang,
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(
        request.text,
        **translate_kwargs,
    )

    detected_language = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else request.source_language
    )

    return ComplianceTranslationResponse(
        translated_text=result.text,
        source_language=request.source_language,
        target_language=request.target_language,
        detected_language=detected_language,
        request_id="",
        metadata={
            "provider": "deepl",
            "source_language_code": source_lang,
            "target_language_code": target_lang,
        },
    )
