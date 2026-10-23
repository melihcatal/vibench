import os
import deepl
from typing import List, Optional
from speech_models import TranslationRequest, TranslationResponse


def translate_script(
    text: str,
    source_lang: str = "en",
    target_lang: str = "es",
    auth_key: Optional[str] = None,
) -> TranslationResponse:
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    translator = deepl.Translator(key)
    result = translator.translate_text(
        text,
        source_lang=source_lang if source_lang != "auto" else None,
        target_lang=target_lang,
    )
    return TranslationResponse(
        translated_text=result.text,
        source_lang=result.detected_source_lang or source_lang,
        target_lang=target_lang,
        character_count=len(text),
    )


def translate_script_batch(
    texts: List[str],
    source_lang: str = "en",
    target_lang: str = "es",
    auth_key: Optional[str] = None,
) -> List[TranslationResponse]:
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    translator = deepl.Translator(key)
    results = translator.translate_text(
        texts,
        source_lang=source_lang if source_lang != "auto" else None,
        target_lang=target_lang,
    )
    responses = []
    for original, result in zip(texts, results):
        responses.append(
            TranslationResponse(
                translated_text=result.text,
                source_lang=result.detected_source_lang or source_lang,
                target_lang=target_lang,
                character_count=len(original),
            )
        )
    return responses
