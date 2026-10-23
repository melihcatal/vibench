import os
import json
import requests
from typing import List, Dict, Any


def summarize_records(records: List[Dict[str, Any]]) -> str:
    texts = []
    for r in records:
        texts.append(f"Title: {r.get('title', 'N/A')}\\nBody: {r.get('body', '')}")
    prompt_text = "\\n---\\n".join(texts)
    prompt = f"Please provide a concise summary of the following document records:\\n\\n{prompt_text}"

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY required")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "grok-beta",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
    }

    response = requests.post(
        "https://api.x.ai/v1/chat/completions", headers=headers, json=data
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
