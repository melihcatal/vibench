import json
import os
from typing import Any, Dict, List, Optional

import requests


BRAVE_SEARCH_API_URL = "https://api.search.brave.com/res/v1/web/search"
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def search_web(query: str, count: int = 5) -> List[Dict[str, Any]]:
    api_key = _require_env("BRAVE_SEARCH_API_KEY")
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }
    params = {"q": query, "count": count}
    response = requests.get(BRAVE_SEARCH_API_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data.get("web", {}).get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            }
        )
    return results


def _build_prompt(query: str, results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    sources = []
    for i, result in enumerate(results, start=1):
        sources.append(
            f"Source {i}: {result.get('title', '')}\nURL: {result.get('url', '')}\nSummary: {result.get('description', '')}"
        )
    user_content = (
        "Create a concise spoken brief from the search results. "
        "Focus on the most relevant facts, keep it natural for audio, and mention uncertainty where appropriate.\n\n"
        f"Query: {query}\n\n"
        + "\n\n".join(sources)
    )
    return [
        {"role": "system", "content": "You write short, accurate spoken news-style briefs based only on provided sources."},
        {"role": "user", "content": user_content},
    ]


def generate_brief(query: str, results: List[Dict[str, Any]]) -> str:
    api_key = _require_env("OPENAI_API_KEY")
    payload = {
        "model": "gpt-4.1-mini",
        "messages": _build_prompt(query, results),
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def synthesize_speech(text: str, output_path: str) -> str:
    api_key = _require_env("OPENAI_API_KEY")
    payload = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": "alloy",
        "format": "mp3",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.post(OPENAI_TTS_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def create_audio_brief(query: str, output_path: str = "brief.mp3", count: int = 5) -> Dict[str, Any]:
    results = search_web(query, count=count)
    brief = generate_brief(query, results)
    audio_path = synthesize_speech(brief, output_path)
    return {"query": query, "results": results, "brief": brief, "audio_path": audio_path}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a spoken brief from retrieved search results.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--output", default="brief.mp3", help="Output MP3 file path")
    parser.add_argument("--count", type=int, default=5, help="Number of search results to retrieve")
    args = parser.parse_args()
    result = create_audio_brief(args.query, output_path=args.output, count=args.count)
    print(json.dumps(result, ensure_ascii=False))
