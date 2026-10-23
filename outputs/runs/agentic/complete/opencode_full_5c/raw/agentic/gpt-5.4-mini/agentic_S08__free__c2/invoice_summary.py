from typing import Any, Dict

from openai import OpenAI


def invoice_summary(extracted: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice data in one sentence: {extracted}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
