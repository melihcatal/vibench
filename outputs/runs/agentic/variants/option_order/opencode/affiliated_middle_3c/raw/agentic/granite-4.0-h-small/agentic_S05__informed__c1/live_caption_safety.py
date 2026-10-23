import asyncio
import json
import requests
from speech_client import get_client
from speech_models import normalize_transcript

# -------------------------------
# Unsafe content check using OpenAI Moderation API
# -------------------------------

# OpenAI credentials must be set in environment variable OPENAI_API_KEY
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

# Endpoint & request payload structure
MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"


def check_content(text: str) -> bool:
    """Return True if text is flagged as unsafe."""
    payload = {
        "input": text,
        "model": "content-moderator",  # placeholder model name
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(MODERATION_ENDPOINT, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Simple heuristic: if any flag appears, consider unsafe
        flags = data.get("results", [{}])[0].get("flagged", False)
        return flags
    except Exception as exc:
        print(json.dumps({"moderation_error": str(exc)}))
        return False


async def live_safety_filter():
    # Placeholder async audio source (microphone)
    async def mic_chunks():
        for i in range(5):
            yield b"utterance_"
            await asyncio.sleep(0.9)

    client = get_client()
    listen_cfg = {"language": "en-US", "punctuation": True}
    source = client.listen(source=mic_chunks(), **listen_cfg)

    async for result in source.listen():
        if result.get("is_final"):
            norm = normalize_transcript(result)
            safe = not check_content(norm["transcript"])
            print(json.dumps({"text": norm["transcript"], "safe": safe}))


if __name__ == "__main__":
    asyncio.run(live_safety_filter())
