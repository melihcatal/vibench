from typing import Any, Dict

from openai import OpenAI


def image_summary(analysis: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this visual analysis in one sentence: {analysis}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
