from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_TEXT_MODEL,
)
from describe_image import describe_image
from vision_models import ImageDescriptionResponse


TRANSLATE_SYSTEM_PROMPT = (
    "You are a translation assistant powered by the OpenAI gpt-4o model. "
    "Translate the provided image description text from its source language "
    "into the specified target language. Preserve all visual details and "
    "maintain accessibility-friendly alt-text style. Return only the translated text."
)

TRANSLATE_USER_PROMPT = (
    "Translate the following image alt-text description into {target_language}:\n\n"
    "{description}\n\n"
    "Source language hint: {source_language}"
)


def translate_alt_text(
    description: str,
    target_language: str,
    source_language: str = "auto",
    model: str = DEFAULT_TEXT_MODEL,
) -> str:
    user_prompt = TRANSLATE_USER_PROMPT.format(
        target_language=target_language,
        description=description,
        source_language=source_language,
    )
    messages = build_vision_messages(
        system_prompt=TRANSLATE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=None,
    )
    return call_vision_api(messages, model=model).strip()


def describe_and_translate(
    image_path: str,
    target_language: str,
    source_language: str = "auto",
    max_length: int = 150,
    detail_level: str = "brief",
    model: str = DEFAULT_TEXT_MODEL,
) -> dict:
    desc_resp = describe_image(
        image_path=image_path,
        max_length=max_length,
        detail_level=detail_level,
    )
    translated = translate_alt_text(
        description=desc_resp.description,
        target_language=target_language,
        source_language=source_language,
        model=model,
    )
    return {
        "image_path": image_path,
        "source_language": source_language,
        "target_language": target_language,
        "original_alt_text": desc_resp.description,
        "translated_alt_text": translated,
    }


def translate_alt_text_batch(
    descriptions: list[str],
    target_language: str,
    source_language: str = "auto",
    model: str = DEFAULT_TEXT_MODEL,
) -> list[str]:
    results: list[str] = []
    for desc in descriptions:
        translated = translate_alt_text(
            description=desc,
            target_language=target_language,
            source_language=source_language,
            model=model,
        )
        results.append(translated)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    lang = sys.argv[2] if len(sys.argv) > 2 else "es"
    result = describe_and_translate(path, lang)
    print(f"Original: {result['original_alt_text']}")
    print(f"Translated ({result['target_language']}): {result['translated_alt_text']}")
