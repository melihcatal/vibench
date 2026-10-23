import os
import sys
from typing import Any, Dict, List

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")


def _client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    kwargs: Dict[str, Any] = {"api_key": api_key}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return OpenAI(**kwargs)


def _build_brief(results: List[Dict[str, Any]], query: str) -> str:
    client = _client()
    prompt = [
        {"role": "system", "content": "You create a concise spoken brief from search results."},
        {"role": "user", "content": f"Query: {query}\nResults: {results}\nWrite a short spoken brief with the most important findings."},
    ]
    response = client.chat.completions.create(model=OPENAI_CHAT_MODEL, messages=prompt)
    return response.choices[0].message.content or ""


def generate_spoken_brief(results: List[Dict[str, Any]], query: str) -> bytes:
    brief_text = _build_brief(results, query)
    client = _client()
    audio = client.audio.speech.create(model=OPENAI_AUDIO_MODEL, voice="alloy", input=brief_text)
    return audio.read()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: retrieval_audio_brief.py <query>")
    query = sys.argv[1]
    results = [{"title": "Example result", "snippet": "Example snippet relevant to the query."}]
    sys.stdout.buffer.write(generate_spoken_brief(results, query))


if __name__ == "__main__":
    main()
