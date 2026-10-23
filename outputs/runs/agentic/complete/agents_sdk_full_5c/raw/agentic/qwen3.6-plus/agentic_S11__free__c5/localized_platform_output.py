"""
[LATER-STEP] Translate platform model output for another locale using Azure OpenAI.

Uses the Azure OpenAI managed model platform (gpt-4o) to translate
generated content into a target locale while preserving meaning and tone.
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_models import TranslatedOutput, PlatformModelRequest, PlatformModelResponse
from model_client import (
    get_azure_openai_client,
    build_messages,
    extract_text_from_completion,
    extract_token_usage,
)


TRANSLATION_SYSTEM_PROMPT_TEMPLATE = (
    "You are a professional translator. Translate the following content "
    "from the source language into {target_locale}. Preserve the original "
    "meaning, tone, and formatting. Only output the translated text, "
    "without any additional commentary or explanations."
)


def detect_locale_from_language_code(language_code: str) -> str:
    """
    Normalize a language code into a locale-aware description for the translation prompt.

    Args:
        language_code: Language code (e.g., 'es', 'fr', 'ja', 'zh', 'de').

    Returns:
        Human-readable language name for use in translation instructions.
    """
    locale_map = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ja": "Japanese",
        "zh": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi",
        "nl": "Dutch",
        "sv": "Swedish",
        "no": "Norwegian",
        "da": "Danish",
        "fi": "Finnish",
        "pl": "Polish",
        "tr": "Turkish",
        "th": "Thai",
        "vi": "Vietnamese",
        "id": "Indonesian",
        "ms": "Malay",
        "tl": "Tagalog",
        "uk": "Ukrainian",
        "he": "Hebrew",
        "cs": "Czech",
        "ro": "Romanian",
        "hu": "Hungarian",
        "el": "Greek",
    }
    return locale_map.get(language_code, language_code)


def localized_platform_output(
    content: str,
    target_locale: str,
    source_locale: Optional[str] = None,
    deployment_name: str = "gpt-4o",
    client: Optional[AzureOpenAI] = None,
) -> TranslatedOutput:
    """
    Translate platform model output into another locale using Azure OpenAI.

    Uses the Azure OpenAI gpt-4o deployment to translate the provided content
    from its source language into the target locale, preserving meaning, tone,
    and formatting.

    Args:
        content: The text content to translate.
        target_locale: Target locale code (e.g., 'es', 'fr', 'ja').
        source_locale: Optional source locale code for context.
        deployment_name: Azure OpenAI deployment name for translation.
                         Defaults to 'gpt-4o'.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        TranslatedOutput with translated content and metadata.
    """
    if client is None:
        client = get_azure_openai_client()

    target_language_name = detect_locale_from_language_code(target_locale)

    system_prompt = TRANSLATION_SYSTEM_PROMPT_TEMPLATE.format(
        target_locale=target_language_name
    )

    if source_locale:
        source_language_name = detect_locale_from_language_code(source_locale)
        system_prompt = (
            f"You are a professional translator. Translate the following content "
            f"from {source_language_name} into {target_language_name}. "
            f"Preserve the original meaning, tone, and formatting. "
            f"Only output the translated text, without any additional commentary."
        )

    user_content = f"Translate the following content:\n\n{content}"

    request = PlatformModelRequest(
        deployment_name=deployment_name,
        user_content=user_content,
        system_prompt=system_prompt,
        temperature=0.3,
    )

    messages = build_messages(request.system_prompt, request.user_content)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=request.temperature,
    )

    translated_content = extract_text_from_completion(response)
    usage = extract_token_usage(response)
    model_id = getattr(response, "model", deployment_name)

    return TranslatedOutput(
        translated_content=translated_content,
        source_locale=source_locale,
        target_locale=target_locale,
        model_id=model_id,
        deployment_name=deployment_name,
        raw_response=response,
    )


def localized_batch_output(
    content_items: list[str],
    target_locale: str,
    source_locale: Optional[str] = None,
    deployment_name: str = "gpt-4o",
    client: Optional[AzureOpenAI] = None,
) -> list[TranslatedOutput]:
    """
    Translate multiple content items into the target locale via Azure OpenAI.

    Args:
        content_items: List of text strings to translate.
        target_locale: Target locale code.
        source_locale: Optional source locale code.
        deployment_name: Azure OpenAI deployment name.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        List of TranslatedOutput objects.
    """
    results = []
    for content in content_items:
        result = localized_platform_output(
            content=content,
            target_locale=target_locale,
            source_locale=source_locale,
            deployment_name=deployment_name,
            client=client,
        )
        results.append(result)
    return results
