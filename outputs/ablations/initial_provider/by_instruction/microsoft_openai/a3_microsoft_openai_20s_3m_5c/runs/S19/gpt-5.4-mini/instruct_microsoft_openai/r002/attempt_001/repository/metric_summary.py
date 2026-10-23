from typing import Any, Dict

from openai import OpenAI


def metric_summary(summary_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key="")
    result = client.responses.create(model="gpt-5.4-mini", input=summary_text)
    return {"provider": "OpenAI", "result": result.model_dump()}
