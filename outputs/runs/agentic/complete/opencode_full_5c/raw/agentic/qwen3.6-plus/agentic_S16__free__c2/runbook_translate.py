import os
import json
import openai
from security_models import TranslationResult


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


client = openai.OpenAI(api_key=OPENAI_API_KEY)


def translate_runbook_text(
    source_text: str, target_language: str = "en", source_language: str = "auto"
) -> TranslationResult:
    lang_instruction = ""
    if source_language != "auto":
        lang_instruction = f"The source text is in {source_language}."
    prompt = (
        f"Translate the following secret-rotation runbook notes from the source language to {target_language}. "
        f"Preserve technical terms, command syntax, and formatting. {lang_instruction}\n\n"
        f"Runbook text:\n{source_text}\n\n"
        f"Provide only the translated text."
    )
    response = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a technical translator specializing in DevOps and security runbooks.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    translated = response.choices[0].message.content.strip()
    return TranslationResult(
        source_text=source_text,
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
        model_used=OPENAI_TRANSLATION_MODEL,
    )


def translate_rotation_runbook(
    secret_id: str = None, target_language: str = "en"
) -> TranslationResult:
    from security_client import describe_secret

    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    metadata = describe_secret(target_id)
    runbook_text = metadata.get("Description", "")
    tags = metadata.get("Tags", [])
    for tag in tags:
        key = tag.get("Key", "")
        value = tag.get("Value", "")
        if "runbook" in key.lower() or "notes" in key.lower():
            runbook_text = f"{runbook_text}\n{key}: {value}"
    if not runbook_text.strip():
        runbook_text = (
            f"Rotation runbook for secret: {target_id}. No additional notes provided."
        )
    return translate_runbook_text(runbook_text, target_language=target_language)


def batch_translate_runbooks(entries: list, target_language: str = "en") -> list:
    results = []
    for entry in entries:
        text = entry.get("text", entry.get("runbook", ""))
        source_lang = entry.get("source_language", "auto")
        result = translate_runbook_text(
            text, target_language=target_language, source_language=source_lang
        )
        results.append(result)
    return results


def generate_multilingual_runbook(
    secret_id: str = None, languages: list = None
) -> dict:
    target_languages = languages or ["en", "es", "fr", "de", "ja"]
    from security_client import describe_secret

    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    metadata = describe_secret(target_id)
    source_text = metadata.get("Description", "")
    translations = {}
    for lang in target_languages:
        try:
            result = translate_runbook_text(source_text, target_language=lang)
            translations[lang] = result.translated_text
        except Exception as e:
            translations[lang] = f"Translation error: {str(e)}"
    return {
        "secret_id": target_id,
        "source_text": source_text,
        "translations": translations,
        "model_used": OPENAI_TRANSLATION_MODEL,
    }


if __name__ == "__main__":
    result = translate_rotation_runbook(target_language="es")
    print(f"Model: {result.model_used}")
    print(f"Source: {result.source_text[:100]}...")
    print(f"Translated: {result.translated_text}")
