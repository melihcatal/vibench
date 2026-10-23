import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _normalize_results(results: Any) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    if not results:
        return normalized
    for item in results:
        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            snippet = str(item.get("snippet", item.get("summary", ""))).strip()
            url = str(item.get("url", item.get("link", ""))).strip()
            normalized.append({"title": title, "snippet": snippet, "url": url})
        else:
            normalized.append({"title": str(item).strip(), "snippet": "", "url": ""})
    return normalized


def build_brief_prompt(query: str, results: List[Dict[str, str]]) -> str:
    lines = [f"Query: {query}", "Retrieved search results:"]
    for idx, result in enumerate(results, 1):
        lines.append(
            f"{idx}. Title: {result['title']} | Snippet: {result['snippet']} | URL: {result['url']}"
        )
    lines.append(
        "Write a concise spoken brief summarizing the most important findings in natural, audio-friendly language. "
        "Keep it under 180 words, avoid bullet points, and mention uncertainty when the results disagree."
    )
    return "\n".join(lines)


def generate_spoken_brief(query: str, results: Any) -> str:
    normalized_results = _normalize_results(results)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You create concise spoken briefs from search results."},
            {"role": "user", "content": build_brief_prompt(query, normalized_results)},
        ],
        "temperature": 0.3,
    }
    response = requests.post(OPENAI_API_URL, headers=_auth_headers(), json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def synthesize_brief_audio(text: str, output_path: str) -> str:
    payload = {"model": OPENAI_TTS_MODEL, "voice": "alloy", "input": text, "format": "mp3"}
    response = requests.post(OPENAI_TTS_URL, headers=_auth_headers(), json=payload, timeout=120)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def create_retrieval_audio_brief(query: str, results: Any, output_path: str) -> Dict[str, str]:
    brief_text = generate_spoken_brief(query, results)
    audio_path = synthesize_brief_audio(brief_text, output_path)
    return {"text": brief_text, "audio_path": audio_path}
