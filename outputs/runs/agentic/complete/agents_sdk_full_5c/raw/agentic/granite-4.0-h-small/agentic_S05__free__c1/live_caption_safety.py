import asyncio
import json
import os
from typing import AsyncGenerator
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import content_safeguard_v1 as content_safeguard

# Provider: Google Cloud Speech-to-Text (hosted API: speech.googleapis.com)
# Provider: Google Cloud Content Safeguard (hosted API: content-safeguard.googleapis.com)
# Ensure GOOGLE_APPLICATION_CREDENTIALS env var points to service account JSON.

# Import helper client builder from shared module
from speech_client import build_streaming_config, create_client as create_speech_client

# Create a single Content Safeguard client (reused across calls)
_sclient = None

def _get_content_safeguard_client() -> content_safeguard.ContentSafeguardClient:
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS env var')
    global _sclient
    if _sclient is None:
        _sclient = content_safeguard.ContentSafeguardClient()
    return _sclient

async def live_caption_safety(
    audio_source: AsyncGenerator[bytes, None],
    language: str = 'en-US',
    threshold: float = 0.8,
) -> AsyncGenerator[bool, None]:
    """
    Streams live audio, transcribes it, then checks each transcript chunk
    for unsafe content using Google Cloud Content Safeguard.

    Args:
        audio_source: async generator yielding audio bytes.
        language: language for speech recognition.
        threshold: confidence score above which a safety check is required.

    Yields:
        bool indicating whether the current caption segment is safe (True) or not safe (False).
    """
    speech_client = create_speech_client()
    config = build_streaming_config(language_code=language)
    # Simple placeholder generator for demo; real code streams continuously.
    # First, collect a chunk of transcript (e.g., first 5 seconds).
    transcript = ''
    async for audio in audio_source:
        transcript += 'placeholder_text_'  # replace with real speech result
        if len(transcript) > 50:  # artificial length limit for demo
            break
    # After transcribing, run content safety analysis.
    safe = True
    if len(transcript) > 0:
        client = _get_content_safeguard_client()
        # Construct a SafeContentRequest using the text (ContentSafeguard supports text input).
        request = content_safeguard.SafeTextRequest(
            content=transcript,
            safety_attributes={'hate_speech': True, 'sexual_content': True, 'violent_content': True}
        )
        response = client.analyze_safe_content(request)
        # Check overall safety score (each attribute returns a score 0-1).
        attrs = response.safety_attributes
        # Combine scores; if any exceed threshold, consider unsafe.
        unsafe_scores = {k: v.score for k, v in attrs.items() if v.score > threshold}
        safe = len(unsafe_scores) == 0
    yield safe

# Demo stub (will not stream audio)
# async def demo():
#     async for safe in live_caption_safety(None):
#         print('Safe:', safe)
#     await demo()