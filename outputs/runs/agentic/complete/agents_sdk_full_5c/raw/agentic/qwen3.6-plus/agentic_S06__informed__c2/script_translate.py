"""Translate narration scripts before synthesis using DeepL API."""

import os
from typing import Optional, List, Dict
import deepl

from speech_models import TTSRequest


def translate_script(
    text: str,
    source_lang: Optional[str] = None,
    target_lang: str = "EN-US",
) -> str:
    """Translate a narration script using DeepL API before TTS synthesis.

    Args:
        text: Source text to translate.
        source_lang: Source language code (e.g., 'DE', 'FR', 'JA'). Auto-detected if None.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'FR', 'JA').

    Returns:
        Translated text ready for TTS synthesis.

    Raises:
        deepl.exceptions.AuthorizationException: If DEEPL_AUTH_KEY is invalid.
        deepl.exceptions.DeepLException: On other API errors.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY environment variable is required. "
            "Set it to your DeepL API key from https://www.deepl.com/"
        )

    translator = deepl.Translator(auth_key)

    translate_params: Dict[str, str] = {"target_lang": target_lang}
    if source_lang:
        translate_params["source_lang"] = source_lang

    result = translator.translate_text(text, **translate_params)
    return result.text


def translate_script_batch(
    texts: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> List[str]:
    """Translate multiple narration scripts in a single DeepL API call.

    Args:
        texts: List of source texts to translate.
        target_lang: Target language code.
        source_lang: Source language code (auto-detected if None).

    Returns:
        List of translated texts.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required.")

    translator = deepl.Translator(auth_key)

    translate_params: Dict[str, str] = {"target_lang": target_lang}
    if source_lang:
        translate_params["source_lang"] = source_lang

    results = translator.translate_text(texts, **translate_params)
    return [r.text for r in results]


def translate_for_tts(
    request: TTSRequest,
    target_lang: str = "EN-US",
) -> TTSRequest:
    """Translate a TTS request's text field using DeepL and return updated request.

    Args:
        request: Original TTSRequest with text to translate.
        target_lang: Target language for DeepL translation.

    Returns:
        Updated TTSRequest with translated text and adjusted language_code.
    """
    translated = translate_script(
        text=request.text,
        target_lang=target_lang,
        source_lang=None,
    )

    return TTSRequest(
        text=translated,
        voice_id=request.voice_id,
        model_id=request.model_id,
        speed=request.speed,
        pitch=request.pitch,
        language_code=target_lang.split("-")[0].lower(),
        output_format=request.output_format,
        stability=request.stability,
        similarity_boost=request.similarity_boost,
    )


if __name__ == "__main__":
    result = translate_script("Willkommen bei unserer Präsentation.", target_lang="EN-US")
    print(f"Translated: {result}")
