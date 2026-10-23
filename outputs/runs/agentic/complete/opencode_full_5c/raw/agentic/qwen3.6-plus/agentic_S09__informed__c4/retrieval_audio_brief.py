import os
import requests
from similarity_score import similarity_score

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def generate_spoken_brief(
    query: str,
    results: list[dict],
    voice_id: str | None = None,
    model_id: str | None = None,
    api_key: str | None = None,
    max_results: int = 5,
) -> bytes:
    key = api_key or os.getenv(ELEVENLABS_API_KEY_ENV)
    if not key:
        raise ValueError(f"{ELEVENLABS_API_KEY_ENV} environment variable is required")
    vid = voice_id or DEFAULT_VOICE_ID
    mid = model_id or DEFAULT_MODEL_ID
    limited_results = results[:max_results]
    scored_results = []
    for item in limited_results:
        doc_text = item.get("text", item.get("content", ""))
        score = item.get("score", similarity_score(query, doc_text))
        scored_results.append((score, doc_text))
    scored_results.sort(key=lambda x: x[0], reverse=True)
    brief_parts = [f"Search results for: {query}"]
    for i, (score, text) in enumerate(scored_results, 1):
        snippet = text[:200] + "..." if len(text) > 200 else text
        brief_parts.append(f"Result {i} (relevance: {score:.2f}): {snippet}")
    brief_text = "\n\n".join(brief_parts)
    url = f"{ELEVENLABS_API_URL}/text-to-speech/{vid}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key,
    }
    payload = {
        "text": brief_text,
        "model_id": mid,
        "output_format": "mp3_44100_128",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.content
