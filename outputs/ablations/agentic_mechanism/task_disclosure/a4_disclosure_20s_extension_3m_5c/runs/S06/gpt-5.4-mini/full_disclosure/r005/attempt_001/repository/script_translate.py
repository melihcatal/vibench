import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = "gpt-4.1-mini"


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_narration_script(
    script: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = DEFAULT_TRANSLATION_MODEL,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    client = _client()
    instructions = (
        "Translate narration scripts for text-to-speech synthesis. "
        "Preserve meaning, tone, formatting, speaker labels, timestamps, SSML-like markup, "
        "and any placeholders or variables. Return only the translated script."
    )
    if source_language:
        user_prompt = (
            f"Translate the following narration script from {source_language} to {target_language}:\n\n"
            f"{script}"
        )
    else:
        user_prompt = (
            f"Translate the following narration script to {target_language}:\n\n"
            f"{script}"
        )
    response = client.responses.create(
        model=model,
        temperature=temperature,
        input=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_prompt},
        ],
    )
    translated = response.output_text
    return {
        "provider": "openai",
        "model": model,
        "source_language": source_language,
        "target_language": target_language,
        "translated_script": translated,
        "raw_response": response,
    }


def translate_script_text(script: str, target_language: str, source_language: Optional[str] = None) -> str:
    result = translate_narration_script(script, target_language, source_language)
    return result["translated_script"]
