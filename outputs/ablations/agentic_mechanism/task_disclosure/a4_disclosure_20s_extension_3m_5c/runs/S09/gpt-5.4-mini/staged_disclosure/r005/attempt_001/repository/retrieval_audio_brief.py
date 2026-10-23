import json
import os
import sys
from typing import List, Dict, Any

import requests


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
OPENAI_TTS_MODEL = os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_API_BASE = "https://api.openai.com/v1"


def _headers() -> Dict[str, str]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def _normalize_results(results: Any) -> List[Dict[str, Any]]:
    if isinstance(results, list):
        return [r for r in results if isinstance(r, dict)]
    if isinstance(results, dict):
        for key in ("results", "items", "data"):
            value = results.get(key)
            if isinstance(value, list):
                return [r for r in value if isinstance(r, dict)]
    raise ValueError("Expected search results as a list or object containing results/items/data")


def build_brief(results: List[Dict[str, Any]]) -> str:
    lines = []
    for idx, item in enumerate(results[:8], start=1):
        title = str(item.get("title") or item.get("name") or item.get("headline") or "Untitled")
        snippet = str(item.get("snippet") or item.get("summary") or item.get("description") or "")
        url = str(item.get("url") or item.get("link") or "")
        lines.append(f"{idx}. {title}\n{snippet}\n{url}".strip())
    prompt = (
        "Create a concise spoken brief from these retrieved search results. "
        "Summarize the main themes, highlight important specifics, and mention uncertainty when appropriate. "
        "Keep it natural for text-to-speech, about 60-90 seconds when spoken.\n\n"
        + "\n\n".join(lines)
    )
    response = requests.post(
        f"{OPENAI_API_BASE}/responses",
        headers=_headers(),
        json={
            "model": OPENAI_CHAT_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("output_text")
    if text:
        return text.strip()
    output = data.get("output", [])
    chunks = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                chunks.append(content.get("text", ""))
    if not chunks:
        raise RuntimeError("No text brief returned from OpenAI")
    return "".join(chunks).strip()


def synthesize_audio(text: str, output_path: str) -> None:
    response = requests.post(
        f"{OPENAI_API_BASE}/audio/speech",
        headers={**_headers(), "Accept": "audio/mpeg"},
        json={
            "model": OPENAI_TTS_MODEL,
            "voice": "alloy",
            "input": text,
            "format": "mp3",
        },
        timeout=120,
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: retrieval_audio_brief.py <search_results_json> <output_audio_path>")
    search_results_path = sys.argv[1]
    output_audio_path = sys.argv[2]
    with open(search_results_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    results = _normalize_results(raw)
    brief = build_brief(results)
    synthesize_audio(brief, output_audio_path)


if __name__ == "__main__":
    main()
