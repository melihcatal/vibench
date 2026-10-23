from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import (
    PlatformMessage,
    PlatformRequest,
    PlatformResponse,
    MessageRole,
    normalize_openai_response,
)

LOCALE_NAME_MAP: dict[str, str] = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "hi": "Hindi",
    "nl": "Dutch",
    "pl": "Polish",
    "sv": "Swedish",
    "tr": "Turkish",
}


def translate_platform_output(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    model: str = "gpt-4o",
    preserve_formatting: bool = True,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> PlatformResponse:
    target_name = LOCALE_NAME_MAP.get(target_locale, target_locale)
    source_name = LOCALE_NAME_MAP.get(source_locale, source_locale)

    formatting_note = (
        " Preserve all formatting, code blocks, and structural elements exactly."
        if preserve_formatting
        else ""
    )

    system_prompt = (
        f"You are a professional translator. Translate the following text from "
        f"{source_name} to {target_name}.{formatting_note} "
        f"Return only the translated text without explanations."
    )

    messages = [
        PlatformMessage(role=MessageRole.SYSTEM, content=system_prompt),
        PlatformMessage(role=MessageRole.USER, content=text),
    ]

    request = PlatformRequest(
        messages=messages,
        model=model,
        temperature=0.3,
        max_tokens=4096,
        stream=False,
    )

    openai_client = client or create_openai_client(config)
    payload = request.to_openai_payload()
    raw_response = openai_client.chat.completions.create(**payload)

    return normalize_openai_response(raw_response)


def localize_platform_output(
    text: str,
    target_locale: str,
    source_locale: str = "en",
    model: str = "gpt-4o",
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> str:
    response = translate_platform_output(
        text=text,
        target_locale=target_locale,
        source_locale=source_locale,
        model=model,
        client=client,
        config=config,
    )
    return response.content


if __name__ == "__main__":
    translated = localize_platform_output(
        text="Hello, welcome to our platform!",
        target_locale="es",
    )
    print(translated)
