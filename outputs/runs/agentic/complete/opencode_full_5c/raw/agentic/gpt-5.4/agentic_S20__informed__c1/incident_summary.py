from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


def summarize_incident(findings: Dict[str, Any], model: str = "gpt-4.1-mini") -> str:
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You summarize production log findings for incident review. Return concise operational prose.",
            },
            {
                "role": "user",
                "content": f"Summarize these error-log findings for incident review: {findings}",
            },
        ],
    )
    return response.output_text
