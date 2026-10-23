import os
from openai import OpenAI
from observability_models import TranslationResult


OPENAI_TRANSLATION_MODEL = "gpt-4o"


def translate_log_message(
    text: str,
    target_language: str = "es",
    source_language: str = "auto",
) -> TranslationResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    language_names = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "pt": "Portuguese",
        "ko": "Korean",
        "it": "Italian",
        "ru": "Russian",
        "ar": "Arabic",
    }
    target_name = language_names.get(target_language, target_language)

    system_prompt = (
        "You are a technical translator specializing in software log messages. "
        "Translate the following log message accurately while preserving technical terms, "
        "error codes, variable names, and structured data formats (JSON, timestamps, IPs, etc.). "
        f"Translate to {target_name}."
    )

    completion = client.chat.completions.create(
        model=OPENAI_TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this log message:\n\n{text}"},
        ],
        max_tokens=200,
        temperature=0.1,
    )

    translated = completion.choices[0].message.content.strip()

    return TranslationResult(
        original_text=text,
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
        model_used=OPENAI_TRANSLATION_MODEL,
    )


def translate_log_messages(
    messages: list[str],
    target_language: str = "es",
    source_language: str = "auto",
) -> list[TranslationResult]:
    results = []
    for msg in messages:
        result = translate_log_message(msg, target_language, source_language)
        results.append(result)
    return results


if __name__ == "__main__":
    sample = "Connection refused: unable to reach database host db-primary.internal:5432 after 3 retries"
    result = translate_log_message(sample, target_language="es")
    print(result.model_dump_json(indent=2))
