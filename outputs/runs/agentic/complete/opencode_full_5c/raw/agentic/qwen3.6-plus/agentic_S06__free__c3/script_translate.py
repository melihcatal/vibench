import os
from speech_client import get_openai_client
from speech_models import TranslationResult


def translate_script(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
) -> TranslationResult:
    client = get_openai_client()
    system_prompt = (
        "You are a professional translator. Translate the given text to the target language. "
        "Preserve tone, style, and formatting. Return only the translation."
    )
    if source_language != "auto":
        system_prompt = (
            f"Translate from {source_language} to {target_language}. {system_prompt}"
        )
    else:
        system_prompt = f"Detect the source language and translate to {target_language}. {system_prompt}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    translated = response.choices[0].message.content.strip()
    detected_lang = source_language
    if source_language == "auto":
        lang_response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Detect the language of this text. Return only the ISO 639-1 code.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.0,
        )
        detected_lang = lang_response.choices[0].message.content.strip()[:2]

    return TranslationResult(
        original_text=text,
        translated_text=translated,
        source_language=detected_lang,
        target_language=target_language,
    )
