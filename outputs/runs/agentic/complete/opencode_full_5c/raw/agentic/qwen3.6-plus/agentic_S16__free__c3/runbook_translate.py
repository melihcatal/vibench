from typing import Optional
import os
import requests

from security_models import TranslationResult


OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_runbook_notes(
    source_text: str, target_language: str = "en", source_language: str = "auto"
) -> TranslationResult:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "You are a technical translator specializing in DevOps and infrastructure runbooks. "
        "Translate the provided runbook notes about secret rotation procedures accurately, "
        "preserving technical terms like secret paths, version numbers, and API endpoints. "
        "Do not translate code blocks, environment variable names, or URL paths."
    )

    if source_language != "auto":
        system_prompt += f" The source text is in {source_language}."

    system_prompt += f" Translate the text to {target_language}."

    payload = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": source_text},
        ],
        "temperature": 0.3,
    }

    resp = requests.post(OPENAI_CHAT_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    result = resp.json()

    choices = result.get("choices", [])
    if not choices:
        raise ValueError("No translation returned from OpenAI API")

    translated_text = choices[0].get("message", {}).get("content", "")

    return TranslationResult(
        source_text=source_text,
        translated_text=translated_text.strip(),
        source_language=source_language,
        target_language=target_language,
        model=OPENAI_TRANSLATION_MODEL,
    )


def translate_runbook_file(
    file_path: str, target_language: str = "en"
) -> TranslationResult:
    with open(file_path, "r") as f:
        content = f.read()
    return translate_runbook_notes(content, target_language)


if __name__ == "__main__":
    sample_runbook = (
        "Secret Rotation Runbook:\n"
        "1. Verify current secret version in Vault at path prod/database/postgres-primary\n"
        "2. Generate new credentials using the rotation script\n"
        "3. Stage the new secret version\n"
        "4. Update application configuration to use the staged version\n"
        "5. Verify connectivity and promote the staged version to active\n"
        "6. Deactivate the previous version after 24-hour monitoring period"
    )
    result = translate_runbook_notes(sample_runbook, target_language="es")
    print(result.to_dict())
