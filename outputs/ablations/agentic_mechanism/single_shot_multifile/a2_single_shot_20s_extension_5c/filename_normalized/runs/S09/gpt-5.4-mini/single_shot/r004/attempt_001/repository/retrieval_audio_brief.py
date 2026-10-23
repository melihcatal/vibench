import os
from typing import Dict, List

import requests


OPENAI_SPEECH_MODEL = os.getenv("OPENAI_SPEECH_MODEL", "gpt-4o-mini-tts")


def retrieval_audio_brief(results: List[Dict[str, str]]) -> Dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    summary_text = " ".join(item.get("snippet", "") for item in results[:5]).strip()
    url = f"{base_url}/audio/speech"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_SPEECH_MODEL, "voice": "alloy", "input": summary_text}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return {"provider": "openai", "model": OPENAI_SPEECH_MODEL, "audio_content_type": response.headers.get("content-type", "audio/mpeg"), "audio_bytes": len(response.content)}


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read())
    print(json.dumps(retrieval_audio_brief(payload["results"])))
