from __future__ import annotations

from typing import Dict, Any

from openai import OpenAI

from vision_models import normalize_description


def image_summary(analysis_results: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize these visual analysis results in one concise sentence: {analysis_results}"
    response = client.responses.create(model="gpt-4o", input=prompt, max_output_tokens=64)
    return normalize_description({"text": response.output_text})
