import os
from security_models import TranslationRequest, TranslationResponse


def translate_runbook(
    source_text: str, target_language: str = "en", source_language: str = "auto"
) -> TranslationResponse:
    request = TranslationRequest(
        source_text=source_text,
        source_language=source_language,
        target_language=target_language,
    )
    return _translate_with_deepl(request)


def _translate_with_deepl(request: TranslationRequest) -> TranslationResponse:
    try:
        import deepl
    except ImportError:
        raise RuntimeError("deepl SDK is required for DeepL API integration")

    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    source_lang = request.source_language if request.source_language != "auto" else None

    result = translator.translate_text(
        request.source_text,
        source_lang=source_lang,
        target_lang=request.target_language,
    )

    return TranslationResponse(
        source_text=request.source_text,
        translated_text=result.text,
        source_language=result.detected_source_lang or request.source_language,
        target_language=request.target_language,
        model_used="deepl",
    )


if __name__ == "__main__":
    result = translate_runbook(
        "Rotate the database credentials every 90 days.", target_language="de"
    )
    print(result.translated_text)
