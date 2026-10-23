# LATER-STEP: live_caption_safety.py
# Check live transcript text for unsafe content

import asyncio
import json
import boto3  # pip install boto3
from speech_models import TranscriptionResult, normalize_message
from typing import AsyncGenerator

# ---------------------------------------------------------------------------
# Content safety client (Amazon Comprehend Toxicity example)
# ---------------------------------------------------------------------------
AWS_REGION = "us-east-1"
comprehend = boto3.client("comprehend", region_name=AWS_REGION)


async def scan_live_captions(
    stream_source: str, provider: str = "deepgram"
) -> AsyncGenerator[bool, None]:
    """Stream audio, transcribe, and yield a boolean indicating if the text is safe.

    Args:
        stream_source: Source of audio (WebSocket URL or file path).
        provider: Speech‑to‑Text provider to use.
    Yields:
        bool: True if safe, False if unsafe.
    """
    async for result in _simulate_stream_provider(provider, stream_source):
        if result.is_final:
            text = result.text
            safe = _is_text_safe(text)
            print(f"[SAFE] {text} => {safe}")
            yield safe


def _is_text_safe(text: str) -> bool:
    """Simple safety check using Amazon Comprehend toxicity detection.
    Returns True when the text is flagged as SAFE; otherwise False.
    """
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response.get("Sentiment")
    # Comprehend's Sentiment is one of: POSITIVE, NEGATIVE, NEUTRAL, MIXED
    # For toxicity we can also call detect_pii_entities or custom classifier.
    # Here we treat NEGATIVE or MIXED as possibly unsafe (simplified).
    return sentiment in ("POSITIVE", "NEUTRAL")


async def _simulate_stream_provider(
    provider: str, source: str
) -> AsyncGenerator[TranscriptionResult, None]:
    """Placeholder async generator mimicking live streaming.
    Replace with actual streaming implementation.
    """
    dummy_chunks = [
        TranscriptionResult(text="I love you", is_final=True),
        TranscriptionResult(text="You are terrible", is_final=True),
        TranscriptionResult(text="Let's have a nice meeting", is_final=True),
    ]
    for chunk in dummy_chunks:
        yield chunk


if __name__ == "__main__":
    asyncio.run(
        list(scan_live_captions("wss://example.com/stream", provider="deepgram"))
    )
