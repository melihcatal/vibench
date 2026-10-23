"""
[LATER-STEP] script_translate.py
Translate narration scripts before synthesis using DeepL API.
"""
from typing import Optional, List, Dict, Any
import os
import deepl
from speech_models import TTSRequest


class ScriptTranslationError(Exception):
    """Raised when translation fails."""
    pass


def get_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create and return a DeepL translator instance."""
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY environment variable is not set and no auth_key provided."
        )
    return deepl.Translator(key)


def translate_script(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> str:
    """
    Translate a narration script using DeepL API.

    Args:
        text: The source text to translate.
        target_lang: Target language code (e.g., "EN-US", "DE", "FR", "JA").
        source_lang: Optional source language code for better accuracy.
        formality: Optional formality level ("more", "less", "default", "prefer_more", "prefer_less").
        auth_key: Optional DeepL API key.
        translator: Optional pre-built DeepL translator.

    Returns:
        Translated text string.
    """
    if translator is None:
        translator = get_deepl_translator(auth_key)

    kwargs: Dict[str, Any] = {}
    if source_lang:
        kwargs["source_lang"] = source_lang
    if formality:
        kwargs["formality"] = formality

    try:
        result = translator.translate_text(text, target_lang=target_lang, **kwargs)
        return result.text
    except deepl.DeepLException as e:
        raise ScriptTranslationError(f"DeepL translation failed: {e}") from e


def translate_script_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> List[str]:
    """
    Translate multiple narration scripts using DeepL batch translation.

    Args:
        texts: List of source texts to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.
        auth_key: Optional DeepL API key.
        translator: Optional pre-built DeepL translator.

    Returns:
        List of translated text strings.
    """
    if translator is None:
        translator = get_deepl_translator(auth_key)

    kwargs: Dict[str, Any] = {}
    if source_lang:
        kwargs["source_lang"] = source_lang

    try:
        results = translator.translate_text(texts, target_lang=target_lang, **kwargs)
        return [r.text for r in results]
    except deepl.DeepLException as e:
        raise ScriptTranslationError(f"DeepL batch translation failed: {e}") from e


def translate_tts_request(
    request: TTSRequest,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> TTSRequest:
    """
    Translate the text in a TTSRequest and return a new request with translated text.

    Args:
        request: Original TTSRequest to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.
        auth_key: Optional DeepL API key.
        translator: Optional pre-built DeepL translator.

    Returns:
        New TTSRequest with translated text and updated language_code.
    """
    translated_text = translate_script(
        text=request.text,
        target_lang=target_lang,
        source_lang=source_lang,
        auth_key=auth_key,
        translator=translator,
    )

    return TTSRequest(
        text=translated_text,
        voice_id=request.voice_id,
        model_id=request.model_id,
        audio_format=request.audio_format,
        speed=request.speed,
        pitch=request.pitch,
        stability=request.stability,
        similarity_boost=request.similarity_boost,
        ssml=request.ssml,
        language_code=target_lang.lower(),
    )


if __name__ == "__main__":
    translated = translate_script(
        text="Welcome to our product demonstration. Today we will show you the key features.",
        target_lang="DE",
        source_lang="EN",
    )
    print(f"Translated: {translated}")
