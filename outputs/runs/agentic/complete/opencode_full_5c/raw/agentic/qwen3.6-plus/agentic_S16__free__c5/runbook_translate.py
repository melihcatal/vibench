import os
import json
import logging
from typing import Optional

import openai
from openai import OpenAI

from security_models import TranslationResult

logger = logging.getLogger(__name__)

OPENAI_TRANSLATION_MODEL = "gpt-4o"
OPENAI_API_ENDPOINT = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    return OpenAI(
        api_key=api_key,
        base_url=OPENAI_API_ENDPOINT,
    )


def translate_runbook_notes(
    source_text: str,
    target_language: str,
    source_language: str = "auto",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> TranslationResult:
    client = get_openai_client()

    system_prompt = (
        "You are a technical translator specializing in security operations and "
        "secret management runbooks. Translate the provided runbook notes accurately, "
        "preserving technical terms, secret identifiers, and operational procedures. "
        "Maintain the original formatting and structure. Do not modify any actual "
        "secret values, API keys, or credentials that may appear in the text."
    )

    language_instruction = f"Translate from {source_language} to {target_language}."
    if source_language == "auto":
        language_instruction = (
            f"Detect the source language and translate to {target_language}."
        )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"{language_instruction}\n\nRunbook notes to translate:\n\n{source_text}",
                },
            ],
            temperature=0.2,
            max_tokens=2000,
        )

        translated_text = response.choices[0].message.content.strip()

        detected_source = source_language
        if source_language == "auto":
            detected_source = (
                response.choices[0].message.content.split("\n")[0]
                if "\n" in response.choices[0].message.content
                else source_language
            )

        result = TranslationResult(
            source_text=source_text,
            translated_text=translated_text,
            source_language=detected_source,
            target_language=target_language,
            model=model,
        )

        logger.info(
            "Translated runbook notes via OpenAI %s: source_lang=%s, target_lang=%s, chars=%d, provider=openai, endpoint=%s",
            model,
            detected_source,
            target_language,
            len(source_text),
            OPENAI_API_ENDPOINT,
        )

        return result

    except Exception as e:
        logger.error(
            "Failed to translate runbook notes via OpenAI %s: error=%s, endpoint=%s",
            model,
            str(e),
            OPENAI_API_ENDPOINT,
        )
        raise


def translate_batch_runbook_notes(
    notes: list[dict],
    target_language: str,
    source_language: str = "auto",
    model: str = OPENAI_TRANSLATION_MODEL,
) -> list[TranslationResult]:
    results = []

    for note in notes:
        text = note.get("text", note.get("content", ""))
        src_lang = note.get("source_language", source_language)

        if text:
            result = translate_runbook_notes(text, target_language, src_lang, model)
            results.append(result)

    return results


def translate_rotation_procedure(
    procedure_text: str,
    target_language: str,
    model: str = OPENAI_TRANSLATION_MODEL,
) -> TranslationResult:
    enhanced_text = (
        f"Secret Rotation Runbook Procedure:\n\n{procedure_text}\n\n"
        f"Note: This is a technical procedure for rotating secrets in a production environment. "
        f"Ensure all technical terms, AWS Secrets Manager references, and operational steps "
        f"are translated accurately."
    )

    return translate_runbook_notes(
        enhanced_text,
        target_language,
        source_language="en",
        model=model,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_runbook = (
        "Step 1: Verify current secret version in AWS Secrets Manager.\n"
        "Step 2: Generate new credential using the rotation Lambda.\n"
        "Step 3: Update the secret with AWSPENDING stage.\n"
        "Step 4: Test new credentials against the target service.\n"
        "Step 5: Promote AWSPENDING to AWSCURRENT stage."
    )
    result = translate_rotation_procedure(sample_runbook, "es")
    print(json.dumps(result.to_dict(), indent=2))
