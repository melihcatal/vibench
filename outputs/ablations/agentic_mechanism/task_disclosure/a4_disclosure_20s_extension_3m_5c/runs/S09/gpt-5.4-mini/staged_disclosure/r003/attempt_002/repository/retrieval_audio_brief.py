import os
import json
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _normalize_results(results: Any) -> List[Dict[str, Any]]:
    if results is None:
        return []
    if isinstance(results, str):
        try:
            parsed = json.loads(results)
            if isinstance(parsed, list):
                return [r for r in parsed if isinstance(r, dict)]
            if isinstance(parsed, dict):
                for key in ("results", "items", "documents", "data"):
                    value = parsed.get(key)
                    if isinstance(value, list):
                        return [r for r in value if isinstance(r, dict)]
        except Exception:
            return [{"text": results}]
        return []
    if isinstance(results, list):
        return [r for r in results if isinstance(r, dict)]
    if isinstance(results, dict):
        for key in ("results", "items", "documents", "data"):
            value = results.get(key)
            if isinstance(value, list):
                return [r for r in value if isinstance(r, dict)]
        return [results]
    return []


def _format_result(item: Dict[str, Any], index: int) -> str:
    title = item.get("title") or item.get("name") or item.get("headline") or f"Result {index}"
    snippet = item.get("snippet") or item.get("summary") or item.get("text") or item.get("description") or ""
    url = item.get("url") or item.get("link") or item.get("source") or ""
    parts = [f"{index}. {title}"]
    if snippet:
        parts.append(f"{snippet}")
    if url:
        parts.append(f"Source: {url}")
    return " ".join(parts)


def build_brief(results: Any, query: Optional[str] = None) -> str:
    items = _normalize_results(results)
    lines = [f"Search brief for: {query}" if query else "Search brief:"]
    if not items:
        lines.append("No search results were provided.")
        return "\n".join(lines)
    for i, item in enumerate(items[:8], start=1):
        lines.append(_format_result(item, i))
    return "\n".join(lines)


def generate_spoken_brief(results: Any, query: Optional[str] = None, model: str = "gpt-5.4-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    brief = build_brief(results, query=query)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Turn search results into a concise spoken brief optimized for text-to-speech. Keep it natural, clear, and under one minute.",
            },
            {"role": "user", "content": brief},
        ],
    )
    return response.output_text


def generate_spoken_brief_audio(results: Any, output_path: str, query: Optional[str] = None, model: str = "gpt-5.4-mini", voice: str = "alloy") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    spoken_text = generate_spoken_brief(results, query=query, model=model)
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=spoken_text,
        format="mp3",
    )
    with open(output_path, "wb") as f:
        f.write(speech.read())
    return output_path
