import os
from typing import Any, List
from mistralai.client import MistralClient

def embedding_job_summary(results: List[dict[str, Any]]) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY required")
    client = MistralClient(api_key=api_key)
    n = len(results)
    texts_preview = [r.get("text", "")[:100] + "..." if len(r.get("text", "")) > 100 else r.get("text", "") for r in results[:5]]
    prompt = f"""Summarize this embedding job:
Number of texts embedded: {n}
Sample texts: {texts_preview}
Assume all embeddings successful. Provide a brief executive summary."""
    messages = [{"role": "user", "content": prompt}]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
