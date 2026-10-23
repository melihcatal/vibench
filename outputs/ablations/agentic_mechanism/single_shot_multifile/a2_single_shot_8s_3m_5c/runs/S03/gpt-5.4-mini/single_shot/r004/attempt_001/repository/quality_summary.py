import os
from typing import Any, Dict

from openai import OpenAI


def summarize_translation_quality(translation_text: str, source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    prompt = f"Review this translation from {source_language} to {target_language} for quality issues such as omissions, mistranslations, awkward phrasing, or terminology drift. Return a concise summary only. Translation: {translation_text}"
    response = client.responses.create(model=model, input=prompt)
    return response.output_text
