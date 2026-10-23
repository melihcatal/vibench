from typing import Any, Dict, Iterable

from openai import OpenAI


def summarize_message_results(results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    items = list(results)
    prompt = {"role": "user", "content": f"Summarize these message processing results in one short paragraph: {items}"}
    response = client.responses.create(model="gpt-4.1-mini", input=[prompt])
    return {"summary": response.output_text, "count": len(items)}
