from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from security_models import ComplianceTranslationResult


def compliance_note_translate(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload["text"])
    source_language = str(payload.get("source_language", "auto"))
    target_language = str(payload.get("target_language", "en"))
    model = payload.get("model", "gpt-4.1-mini")
    client = OpenAI(api_key=payload.get("openai_api_key"))
    prompt = f"Translate the following encryption or compliance note from {source_language} to {target_language}:\n\n{text}"
    response = client.responses.create(model=model, input=prompt)
    translated_text = response.output_text
    result = ComplianceTranslationResult(
        provider="openai",
        model=model,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
    )
    return result.to_dict()
