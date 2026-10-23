import os
from deepl import Translator
from translation_models import TranslationRequest, TranslationResponse
from translation_client import get_deepl_client, normalize_language_code


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)

    result = client.translate_text(
        request.source_text,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang,
    )

    return TranslationResponse(
        translated_text=result.text,
        source_lang=result.detected_source_lang or request.source_lang,
        target_lang=target_lang,
        confidence=1.0,
    )


if __name__ == "__main__":
    req = TranslationRequest(
        source_text="Hello, how are you?",
        source_lang="en",
        target_lang="fr",
    )
    resp = translate_text(req)
    print(resp.translated_text)
