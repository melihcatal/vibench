import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = "gpt-4.1-mini"


@dataclass(frozen=True)
class ScriptTranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    model: str = DEFAULT_TRANSLATION_MODEL


def translate_script(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = DEFAULT_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    client_kwargs = {"api_key": api_key or os.getenv("OPENAI_API_KEY")}
    resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")
    if resolved_base_url is not None:
        client_kwargs["base_url"] = resolved_base_url
    client = OpenAI(**client_kwargs)
    system_prompt = "You translate narration scripts for speech synthesis. Preserve meaning, names, formatting, and line breaks. Return only the translated text."
    if source_language:
        user_prompt = f"Translate the following narration script from {source_language} to {target_language}:\n\n{text}"
    else:
        user_prompt = f"Translate the following narration script to {target_language}:\n\n{text}"
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.output_text.strip()
