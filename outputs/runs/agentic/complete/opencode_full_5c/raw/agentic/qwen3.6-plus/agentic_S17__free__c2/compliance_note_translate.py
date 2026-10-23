import os
import sys
import json
from typing import Dict, Any, Optional

from openai import OpenAI

from security_models import ComplianceNoteTranslation


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def translate_compliance_note(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
    context: Optional[str] = None,
) -> ComplianceNoteTranslation:
    client = get_openai_client()
    system_prompt = (
        "You are a professional translator specializing in encryption, "
        "data security, and compliance documentation. Translate the provided "
        "text accurately while preserving technical terminology, regulatory "
        "references, and compliance-specific language. Maintain the original "
        "tone and formality level."
    )
    if context:
        system_prompt += f"\n\nAdditional context: {context}"
    user_prompt = text
    if source_language != "auto":
        user_prompt = f"[Source: {source_language}] {text}"
    user_prompt += f"\n\nTranslate to: {target_language}"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    translated = response.choices[0].message.content
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return ComplianceNoteTranslation(
        original_text=text,
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
        model=model,
        usage=usage,
    )


def translate_compliance_notes_batch(
    texts: list,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
    context: Optional[str] = None,
) -> list:
    results = []
    for text in texts:
        result = translate_compliance_note(
            text, target_language, source_language, model, context
        )
        results.append(result)
    return results


def main():
    text = sys.stdin.read()
    if not text.strip():
        print("Error: No compliance note text provided on stdin", file=sys.stderr)
        sys.exit(1)
    target_language = os.environ.get("TARGET_LANGUAGE", "en")
    source_language = os.environ.get("SOURCE_LANGUAGE", "auto")
    model = os.environ.get("TRANSLATION_MODEL", "gpt-4o-mini")
    context = os.environ.get("TRANSLATION_CONTEXT")
    result = translate_compliance_note(
        text, target_language, source_language, model, context
    )
    output = {
        "original_text": result.original_text,
        "translated_text": result.translated_text,
        "source_language": result.source_language,
        "target_language": result.target_language,
        "model": result.model,
        "usage": result.usage,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
