import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


DEFAULT_BRIEF_MODEL = os.environ.get("OPENAI_AUDIO_BRIEF_MODEL", "gpt-4o-mini")
DEFAULT_TTS_MODEL = os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.environ.get("OPENAI_TTS_VOICE", "alloy")


@dataclass(frozen=True)
class RetrievedResult:
    title: str
    snippet: str
    score: Optional[float] = None
    url: Optional[str] = None


def _client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def _normalize_results(results: Iterable[Dict[str, Any]]) -> List[RetrievedResult]:
    normalized: List[RetrievedResult] = []
    for item in results:
        normalized.append(
            RetrievedResult(
                title=str(item.get("title") or item.get("name") or "Untitled"),
                snippet=str(item.get("snippet") or item.get("summary") or item.get("text") or ""),
                score=item.get("score"),
                url=item.get("url"),
            )
        )
    return normalized


def _build_brief_prompt(query: str, results: List[RetrievedResult]) -> str:
    lines = [f"Query: {query}", "Retrieved results:"]
    for i, item in enumerate(results, start=1):
        parts = [f"{i}. {item.title}"]
        if item.score is not None:
            parts.append(f"score={item.score}")
        if item.url:
            parts.append(f"url={item.url}")
        if item.snippet:
            parts.append(f"snippet={item.snippet}")
        lines.append(" | ".join(parts))
    lines.append("Write a concise spoken brief for text-to-speech. Use natural language, avoid bullet points, and mention the most relevant findings first.")
    return "\n".join(lines)


def generate_spoken_brief(query: str, results: Iterable[Dict[str, Any]], model: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    client = _client(api_key=api_key)
    model_name = model or DEFAULT_BRIEF_MODEL
    normalized = _normalize_results(results)
    prompt = _build_brief_prompt(query, normalized)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You create short spoken briefs from search results."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    brief_text = (response.choices[0].message.content or "").strip()
    audio_response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=DEFAULT_TTS_VOICE,
        input=brief_text,
        format="mp3",
    )
    audio_bytes = audio_response.read()
    return {"query": query, "brief_text": brief_text, "audio": audio_bytes, "audio_format": "mp3", "model": model_name, "tts_model": DEFAULT_TTS_MODEL, "voice": DEFAULT_TTS_VOICE}


def main() -> None:
    import json
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: python retrieval_audio_brief.py <query> <results-json>")
    query = sys.argv[1]
    results = json.loads(sys.argv[2])
    brief = generate_spoken_brief(query, results)
    print(json.dumps({k: v if k != "audio" else f"<{len(v)} bytes>" for k, v in brief.items()}))


if __name__ == "__main__":
    main()
