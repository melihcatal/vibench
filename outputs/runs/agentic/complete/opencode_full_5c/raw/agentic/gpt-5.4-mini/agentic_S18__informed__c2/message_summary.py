from typing import Any, Dict, List

from openai import OpenAI


def message_summary(messages: List[Dict[str, Any]], model: str = "gpt-5.4-mini") -> Dict[str, Any]:
    client = OpenAI()
    prompt = {"messages": messages}
    response = client.responses.create(model=model, input=str(prompt))
    return {"provider": "openai", "model": model, "summary": response.output_text}
