import os
import requests
from security_models import TranslationResult


OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-mini"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def translate_runbook_notes(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = None,
) -> TranslationResult:
    model = model or DEFAULT_TRANSLATION_MODEL
    api_key = get_openai_api_key()

    system_prompt = (
        "You are a technical translator specializing in DevOps, security, and infrastructure runbooks. "
        "Translate the provided text accurately while preserving technical terms, secret names, "
        "ARNs, and configuration values. Do not translate code blocks, environment variable names, "
        "or provider-specific identifiers."
    )

    if source_language == "auto":
        user_prompt = (
            f"Translate the following runbook notes to {target_language}:\n\n{text}"
        )
    else:
        user_prompt = f"Translate the following runbook notes from {source_language} to {target_language}:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,
    }

    response = requests.post(OPENAI_CHAT_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()

    translated_text = result["choices"][0]["message"]["content"].strip()

    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        model=model,
    )


def translate_batch_runbook_notes(
    entries: list, target_language: str = "en", model: str = None
) -> list:
    model = model or DEFAULT_TRANSLATION_MODEL
    results = []
    for entry in entries:
        text = entry.get("text", "")
        source_lang = entry.get("source_language", "auto")
        if text:
            result = translate_runbook_notes(
                text, target_language, source_lang, model=model
            )
            results.append(result)
    return results


def translate_rotation_runbook(
    secret_id: str, runbook_text: str, target_language: str = "en", model: str = None
) -> dict:
    result = translate_runbook_notes(runbook_text, target_language, model=model)
    return {
        "secret_id": secret_id,
        "translation": result.to_dict(),
    }


if __name__ == "__main__":
    sample_text = (
        "Step 1: Verify the secret arn:aws:secretsmanager:us-east-1:123456789:secret:prod/api/payment-key exists.\n"
        "Step 2: Trigger rotation using the Lambda function rotate-secrets-prod.\n"
        "Step 3: Monitor CloudWatch logs for rotation completion.\n"
        "Step 4: Validate the new secret version in AWSCURRENT stage."
    )
    result = translate_runbook_notes(sample_text, target_language="es")
    print(result.to_dict())
