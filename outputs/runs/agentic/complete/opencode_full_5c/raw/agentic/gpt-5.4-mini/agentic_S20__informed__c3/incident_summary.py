from typing import Any, Dict, List

from openai import OpenAI


def summarize_incident(findings: List[Dict[str, Any]]) -> str:
    client = OpenAI()
    model = "gpt-5.4-mini"
    prompt = f"Summarize the incident findings for review: {findings}"
    response = client.responses.create(model=model, input=prompt)
    return response.output_text
