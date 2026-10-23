import os
from typing import Any, Dict, List

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def summarize_translation_quality_issues(translations: List[Dict[str, Any]]) -> str:
    client = _client()
    prompt = (
        "Summarize the main translation quality issues in the following data. "
        "Focus on accuracy, fluency, terminology, omissions, additions, and consistency. "
        "Return a concise plain-text summary. Data: "
        f"{translations}"
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text
