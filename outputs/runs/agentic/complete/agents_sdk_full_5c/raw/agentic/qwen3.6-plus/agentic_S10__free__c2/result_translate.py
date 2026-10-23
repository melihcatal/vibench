"""
Translate generated model output to a target language.
Provider: OpenAI - https://platform.openai.com
Model: gpt-4o (openai-gpt4o family) - used as a translation engine
"""

from typing import Optional
from model_client import get_openai_client, resolve_model_family, DEFAULT_SUMMARIZE_MODEL
from model_models import (
    LLMRequest,
    LLMResponse,
    normalize_system_user_messages,
)


TRANSLATION_SYSTEM_PROMPT = (
    "You are a professional translator. Translate the provided text from the source "
    "language to the target language. Preserve the original meaning, tone, and style. "
    "Only output the translated text with no additional commentary or explanations."
)

LANGUAGE_CODES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "hi": "Hindi",
    "it": "Italian",
}


def resolve_language_name(code: str) -> str:
    """Map an ISO language code to its full name for the translation prompt."""
    return LANGUAGE_CODES.get(code, code)


def translate_output(
    text: str,
    target_language: str = "es",
    source_language: Optional[str] = None,
    model: str = DEFAULT_SUMMARIZE_MODEL,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Translate model-generated text to a target language using the OpenAI gpt-4o model
    at api.openai.com.

    Args:
        text: The text to translate.
        target_language: ISO language code or language name for the target.
        source_language: Optional source language code or name. If None, auto-detect.
        model: OpenAI model identifier (default: gpt-4o).
        temperature: Sampling temperature for translation.
        api_key: Optional override for OPENAI_API_KEY.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        LLMResponse containing the translated text.
    """
    target_name = resolve_language_name(target_language)

    if source_language:
        source_name = resolve_language_name(source_language)
        lang_instruction = f"Translate the following text from {source_name} to {target_name}."
    else:
        lang_instruction = f"Translate the following text to {target_name}. Detect the source language automatically."

    system_prompt = TRANSLATION_SYSTEM_PROMPT
    user_prompt = f"{lang_instruction}\n\nText to translate:\n{text}"

    messages = normalize_system_user_messages(system_prompt, user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


def translate_with_formatting_preservation(
    text: str,
    target_language: str = "fr",
    model: str = DEFAULT_SUMMARIZE_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Translate text while preserving markdown formatting, code blocks, and structure,
    using OpenAI's gpt-4o model.

    Args:
        text: The formatted text to translate.
        target_language: Target language code.
        model: OpenAI model identifier.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        LLMResponse with the translated, formatted text.
    """
    target_name = resolve_language_name(target_language)
    system_prompt = (
        f"You are a professional translator. Translate the following text to {target_name}. "
        "Preserve all markdown formatting, code blocks, lists, and structural elements. "
        "Only translate the human-readable text content; do not translate code, URLs, "
        "or technical identifiers. Output only the translated text."
    )

    user_prompt = f"Translate this text to {target_name}:\n\n{text}"
    messages = normalize_system_user_messages(system_prompt, user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=0.2,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog. This is a test sentence for translation."
    result = translate_output(text=sample, target_language="es")
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Translation: {result.text}")
