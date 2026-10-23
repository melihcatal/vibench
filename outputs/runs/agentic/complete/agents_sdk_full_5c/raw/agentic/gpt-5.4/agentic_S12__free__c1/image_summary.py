from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from vision_models import coerce_summary


OPENAI_PROVIDER = "openai"
OPENAI_MODEL = "gpt-4.1-mini"


def image_summary(analysis_results: Dict[str, Any]) -> str:
    summary = coerce_summary(analysis_results)
    prompt = {
        "labels": summary.labels,
        "description": summary.description,
        "extracted_text": summary.extracted_text,
        "safety_flags": summary.safety_flags,
    }
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Summarize this image analysis in 2 concise sentences: {prompt}"}
                ],
            }
        ],
        max_output_tokens=120,
    )
    return response.output_text.strip()
