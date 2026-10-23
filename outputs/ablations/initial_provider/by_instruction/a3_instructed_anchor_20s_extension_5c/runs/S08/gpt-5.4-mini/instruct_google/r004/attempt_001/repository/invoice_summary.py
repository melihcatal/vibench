import json
from typing import Any, Dict

from openai import OpenAI


def invoice_summary(payload: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this invoice in one sentence: {json.dumps(payload, ensure_ascii=False)}",
    )
    return response.output_text
