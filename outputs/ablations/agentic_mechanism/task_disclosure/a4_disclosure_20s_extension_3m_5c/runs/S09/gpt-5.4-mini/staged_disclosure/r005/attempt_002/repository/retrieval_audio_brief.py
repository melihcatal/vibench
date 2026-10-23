import os
from typing import List, Dict, Any

from openai import OpenAI


def build_brief(search_results: List[Dict[str, Any]]) -> str:
    lines = []
    for i, item in enumerate(search_results[:5], 1):
        title = str(item.get("title", "Untitled")).strip()
        snippet = str(item.get("snippet", item.get("summary", ""))).strip()
        url = str(item.get("url", "")).strip()
        parts = [f"{i}. {title}"]
        if snippet:
            parts.append(snippet)
        if url:
            parts.append(url)
        lines.append(" - ".join(parts))
    if not lines:
        return "No search results were retrieved."
    return "\n".join(lines)


def generate_spoken_brief(search_results: List[Dict[str, Any]], topic: str = "") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Turn the following retrieved search results into a concise spoken brief. "
        "Use natural spoken language, keep it under 90 seconds, and mention only the most relevant points.\n\n"
        f"Topic: {topic}\n\n"
        f"Search results:\n{build_brief(search_results)}"
    )
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You create concise spoken briefings from retrieved information."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
