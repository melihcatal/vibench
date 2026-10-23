import json
from collections import Counter
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def summarize_messages(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    items = list(records)
    text = json.dumps(items, sort_keys=True)
    prompt = f"Summarize these message processing results concisely: {text}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": response.output_text, "count": len(items), "provider": "openai"}
