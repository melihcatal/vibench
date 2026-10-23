import os
from typing import Iterable, List, Mapping, Any

import openai


def _normalize_results(results: Iterable[Mapping[str, Any]]) -> List[str]:
    lines = []
    for item in results:
        title = str(item.get("title", "")).strip()
        snippet = str(item.get("snippet", item.get("text", ""))).strip()
        url = str(item.get("url", "")).strip()
        parts = [p for p in [title, snippet, url] if p]
        if parts:
            lines.append(". ".join(parts))
    return lines


def generate_spoken_brief(results: Iterable[Mapping[str, Any]], question: str) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    context = _normalize_results(results)
    prompt = (
        "You are creating a short spoken brief for a voice assistant. "
        "Summarize the retrieved search results in a conversational way, "
        "prioritizing the most relevant items and avoiding citations or bullet points. "
        f"Question: {question}\n"
        f"Results:\n{chr(10).join(f'- {line}' for line in context)}"
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text.strip()
