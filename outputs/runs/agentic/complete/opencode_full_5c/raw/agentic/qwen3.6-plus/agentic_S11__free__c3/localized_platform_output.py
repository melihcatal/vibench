from __future__ import annotations

from typing import Dict, List, Optional

from model_client import get_platform_client
from model_models import TranslationResult, normalize_messages


LOCALE_PROMPTS = {
    "es": "Translate the following text to Spanish. Provide only the translation without any explanation:",
    "fr": "Translate the following text to French. Provide only the translation without any explanation:",
    "de": "Translate the following text to German. Provide only the translation without any explanation:",
    "ja": "Translate the following text to Japanese. Provide only the translation without any explanation:",
    "zh": "Translate the following text to Chinese. Provide only the translation without any explanation:",
    "pt": "Translate the following text to Portuguese. Provide only the translation without any explanation:",
    "it": "Translate the following text to Italian. Provide only the translation without any explanation:",
    "ko": "Translate the following text to Korean. Provide only the translation without any explanation:",
    "ar": "Translate the following text to Arabic. Provide only the translation without any explanation:",
    "ru": "Translate the following text to Russian. Provide only the translation without any explanation:",
    "hi": "Translate the following text to Hindi. Provide only the translation without any explanation:",
}


def get_translation_prompt(target_locale: str) -> str:
    return LOCALE_PROMPTS.get(
        target_locale,
        f"Translate the following text to {target_locale}. Provide only the translation without any explanation:",
    )


def localize_platform_output(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    model_id: str = "gpt-4o",
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> TranslationResult:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    translation_prompt = get_translation_prompt(target_locale)
    messages = normalize_messages(
        prompt=text,
        system_prompt=translation_prompt,
    )

    from model_models import PlatformRequest

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        stream=False,
    )

    response = client.chat_completion(request)

    return TranslationResult(
        translated_text=response.content.strip(),
        source_locale=source_locale,
        target_locale=target_locale,
        model_id=response.model_id,
        usage=response.usage,
        raw_response=response.raw_response,
    )


def localize_multiple(
    text: str,
    target_locales: List[str],
    source_locale: str = "en",
    model_id: str = "gpt-4o",
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> Dict[str, TranslationResult]:
    results = {}
    for locale in target_locales:
        result = localize_platform_output(
            text=text,
            target_locale=locale,
            source_locale=source_locale,
            model_id=model_id,
            temperature=temperature,
            api_key=api_key,
            organization=organization,
            project=project,
        )
        results[locale] = result
    return results


def translate_with_context(
    text: str,
    target_locale: str,
    context: Optional[str] = None,
    source_locale: str = "en",
    model_id: str = "gpt-4o",
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> TranslationResult:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    system_parts = [get_translation_prompt(target_locale)]
    if context:
        system_parts.append(f"Context for translation: {context}")
    system_prompt = " ".join(system_parts)

    messages = normalize_messages(
        prompt=text,
        system_prompt=system_prompt,
    )

    from model_models import PlatformRequest

    request = PlatformRequest(
        model_id=model_id,
        messages=messages,
        temperature=temperature,
        stream=False,
    )

    response = client.chat_completion(request)

    return TranslationResult(
        translated_text=response.content.strip(),
        source_locale=source_locale,
        target_locale=target_locale,
        model_id=response.model_id,
        usage=response.usage,
        raw_response=response.raw_response,
    )
