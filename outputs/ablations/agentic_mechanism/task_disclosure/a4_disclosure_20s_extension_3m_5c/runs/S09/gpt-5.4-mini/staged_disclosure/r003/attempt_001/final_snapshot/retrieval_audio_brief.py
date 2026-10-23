import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


def _normalize_results(results: Any) -> List[Dict[str, Any]]:
    if results is None:
        return []
    if isinstance(results, dict):
        if "results" in results and isinstance(results["results"], list):
            items = results["results"]
        elif "items" in results and isinstance(results["items"], list):
            items = results["items"]
        else:
            items = [results]
    elif isinstance(results, list):
        items = results
    else:
        items = [results]

    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
        else:
            normalized.append({"text": str(item)})
    return normalized


def _format_search_results(results: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, item in enumerate(results, start=1):
        title = item.get("title") or item.get("name") or item.get("headline") or "Untitled"
        url = item.get("url") or item.get("link") or item.get("source") or ""
        snippet = item.get("snippet") or item.get("summary") or item.get("text") or ""
        parts = [f"{idx}. {title}"]
        if url:
            parts.append(f"{url}")
        if snippet:
            parts.append(f"{snippet}")
        lines.append(" - ".join(parts))
    return "\n".join(lines) if lines else "No retrieved results provided."


def generate_spoken_brief(retrieved_results: Any, topic: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = _normalize_results(retrieved_results)
    results_text = _format_search_results(normalized)
    topic_text = topic or "the search query"

    prompt = (
        "You are a concise audio news reader. "
        f"Create a spoken brief about {topic_text} using only the retrieved results below. "
        "Write in natural speech, with a clear opening, 3 to 5 key points, and a short closing. "
        "Avoid bullet points, markdown, and citations. Keep it under 180 words.\n\n"
        f"Retrieved results:\n{results_text}"
    )

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text.strip()


if __name__ == "__main__":
    import json
    import sys

    payload = sys.stdin.read().strip()
    data = json.loads(payload) if payload else {}
    print(generate_spoken_brief(data.get("results", data), data.get("topic")))
