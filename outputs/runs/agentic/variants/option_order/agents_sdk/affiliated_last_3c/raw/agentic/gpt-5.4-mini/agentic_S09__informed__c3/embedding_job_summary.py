from __future__ import annotations

from typing import Dict, Iterable, List

from openai import OpenAI

DEFAULT_MODEL = "gpt-4.1-mini"


def summarize_embedding_job(results: List[Dict[str, object]], model: str = DEFAULT_MODEL) -> str:
    client = OpenAI()
    counts = {
        "processed": len(results),
        "success": sum(1 for item in results if item.get("status") == "success"),
        "failed": sum(1 for item in results if item.get("status") != "success"),
    }
    prompt = (
        "Summarize the following OpenAI embedding job results in a concise operational report. "
        f"Counts: {counts}. Results: {results}"
    )
    response = client.responses.create(model=model, input=prompt)
    return response.output_text
