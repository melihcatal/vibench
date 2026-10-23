from __future__ import annotations

from typing import Optional

from speech_client import get_openai_client, resolve_translation_model
from speech_models import TranslationResult


def translate_script(
    script_text: str,
    target_language: str,
    source_language: str = "auto",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TranslationResult:
    resolved_model = resolve_translation_model(model)
    client = get_openai_client(api_key)
    prompt = (
        f"Translate the narration script from {source_language} to {target_language}. "
        "Preserve timing cues, speaker labels, and pronunciation-critical proper nouns."
    )
    response = client.responses.create(
        model=resolved_model,
        input=[
            {
                "role": "system",
                "content": "You are a professional localization translator for voice narration scripts.",
            },
            {"role": "user", "content": f"{prompt}\n\nScript:\n{script_text}"},
        ],
    )
    return TranslationResult(
        translated_text=response.output_text,
        source_language=source_language,
        target_language=target_language,
        model=resolved_model,
    )
