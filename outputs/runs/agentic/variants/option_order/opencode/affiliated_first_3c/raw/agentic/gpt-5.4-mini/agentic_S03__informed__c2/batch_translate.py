from deepl import Translator

from translation_client import (
    create_translation_client,
    load_translation_config,
    normalize_language_code,
)
from translation_models import (
    BatchTranslationRequest,
    TranslationResult,
    normalize_translated_text,
)


def batch_translate(
    texts: list[str], source_lang: str | None = None, target_lang: str = "EN-US"
) -> list[str]:
    config = load_translation_config(source_lang=source_lang, target_lang=target_lang)
    client: Translator = create_translation_client(config)
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=normalize_language_code(source_lang),
        target_lang=normalize_language_code(target_lang) or target_lang,
    )
    results = client.translate_text(
        request.texts, target_lang=request.target_lang, source_lang=request.source_lang
    )
    return [normalize_translated_text(item) for item in results]
