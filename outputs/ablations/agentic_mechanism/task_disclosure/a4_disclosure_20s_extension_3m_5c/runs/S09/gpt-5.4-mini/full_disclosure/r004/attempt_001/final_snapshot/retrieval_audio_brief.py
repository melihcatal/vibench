import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _format_results(results: List[Dict[str, Any]]) -> str:
    lines = []
    for i, result in enumerate(results, start=1):
        title = str(result.get("title", "Untitled"))
        snippet = str(result.get("snippet", result.get("text", "")))
        source = str(result.get("source", result.get("url", "")))
        parts = [f"{i}. {title}"]
        if snippet:
            parts.append(snippet)
        if source:
            parts.append(f"Source: {source}")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def generate_spoken_brief(results: List[Dict[str, Any]], topic: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    brief_context = _format_results(results)
    topic_text = topic or "the search results"
    prompt = (
        f"Create a concise spoken brief about {topic_text} using the retrieved results below. "
        "Write in natural, audio-friendly language, highlight the most important takeaways, "
        "and keep it to about 60 to 120 words.\n\n"
        f"Retrieved results:\n{brief_context}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text.strip()
