from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def quality_summary(
    items: Iterable[Mapping[str, Any]], target_language: str
) -> Dict[str, Any]:
    client = OpenAI()
    payload: List[Dict[str, Any]] = [dict(item) for item in items]
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize translation quality issues and return JSON with keys summary, issues, and risk_level.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Target language: {target_language}\nTranslation review data: {payload}",
                    }
                ],
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODEL,
        "summary": response.output_text,
        "response_id": response.id,
    }
