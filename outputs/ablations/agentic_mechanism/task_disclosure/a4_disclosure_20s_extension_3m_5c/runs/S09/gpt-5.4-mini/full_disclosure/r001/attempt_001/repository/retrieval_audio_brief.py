from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


@dataclass(frozen=True)
class RetrievedResult:
    title: str
    snippet: str
    source: str | None = None
    url: str | None = None

    @classmethod
    def from_obj(cls, obj: Any) -> "RetrievedResult":
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, dict):
            return cls(
                title=str(obj.get("title", "")),
                snippet=str(obj.get("snippet", obj.get("text", ""))),
                source=obj.get("source"),
                url=obj.get("url"),
            )
        return cls(title=str(obj), snippet=str(obj))


def _normalize_results(results: Iterable[Any]) -> list[RetrievedResult]:
    return [RetrievedResult.from_obj(item) for item in results]


def _build_prompt(query: str, results: Sequence[RetrievedResult]) -> str:
    lines = [f"Query: {query}", "Retrieved results:"]
    for i, item in enumerate(results, 1):
        parts = [f"{i}. {item.title}" if item.title else f"{i}."]
        if item.source:
            parts.append(f"Source: {item.source}")
        if item.url:
            parts.append(f"URL: {item.url}")
        if item.snippet:
            parts.append(f"Snippet: {item.snippet}")
        lines.append(" | ".join(parts))
    lines.append(
        "Write a brief spoken-style summary in 2-4 short paragraphs. "
        "Be concise, natural, and suitable for text-to-speech. "
        "Mention the most relevant findings first and avoid bullet points."
    )
    return "\n".join(lines)


def generate_spoken_brief(query: str, results: Iterable[Any], api_key: str | None = None) -> str:
    normalized = _normalize_results(results)
    prompt = _build_prompt(query, normalized)
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You turn retrieved search results into a spoken brief."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("results_json")
    args = parser.parse_args()
    results = json.loads(args.results_json)
    print(generate_spoken_brief(args.query, results))


if __name__ == "__main__":
    main()
