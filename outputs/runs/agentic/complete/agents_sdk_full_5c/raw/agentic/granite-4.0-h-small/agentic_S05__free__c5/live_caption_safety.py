# live_caption_safety.py
import asyncio
import json
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
import re

# Simple profanity filter (regex list) – replace with a more robust solution if needed
PROFANITY_PATTERNS = [
    re.compile(r"\bdum[a-z]*\b", re.IGNORECASE),  # example word
    re.compile(r"\bkill\b", re.IGNORECASE),
    re.compile(r"\bweapon\b", re.IGNORECASE),
]

async def safe_captions(caption_stream: asyncio.Queue):
    """Consumes caption chunks from `caption_stream` and filters out unsafe text.
    Yields only cleaned captions.
    """
    client = get_speech_client()
    cfg = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    stream_cfg = types.StreamingRecognitionConfig(
        config=cfg,
        interim_results=True,
    )

    # Placeholder audio generator
    async def audio_gen():
        for _ in range(5):
            yield b""  # placeholder chunk
            await asyncio.sleep(0.3)

    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_gen())
    responses = client.streaming_recognize(stream_cfg, requests)
    for resp in responses:
        for result in resp.results:
            if result.is_final:
                raw = result.alternatives[0].transcript
                cleaned = raw
                for pat in PROFANITY_PATTERNS:
                    cleaned = pat.sub("[REDACTED]", cleaned)
                if cleaned != raw:
                    print(f"[Safety] Detected unsafe term, replaced with [REDACTED]")
                print(f"[Safe Caption] {cleaned}")
    return

if __name__ == "__main__":
    q = asyncio.Queue()
    asyncio.run(safe_captions(q))
