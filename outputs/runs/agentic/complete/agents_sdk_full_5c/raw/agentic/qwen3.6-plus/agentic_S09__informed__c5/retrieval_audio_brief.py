"""
[LATER-STEP] Generate a spoken brief from retrieved search results.
Provider: ElevenLabs Text to Speech API
SDK: elevenlabs (REST via requests)
Auth: ELEVENLABS_API_KEY
"""

from __future__ import annotations

import io
import os
from dataclasses import dataclass, field
from typing import List, Optional

import requests


ELEVENLABS_API_HOST = "api.elevenlabs.io"
ELEVENLABS_TTS_URL = f"https://{ELEVENLABS_API_HOST}/v1/text-to-speech"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - default ElevenLabs voice


@dataclass
class AudioBrief:
    """Generated spoken brief from search results."""
    text_content: str
    voice_id: str
    audio_bytes: bytes
    model_id: str = "eleven_multilingual_v2"
    duration_estimate_ms: int = 0


def build_brief_text(
    query: str,
    top_results: List[str],
    scores: Optional[List[float]] = None,
    max_results: int = 3,
) -> str:
    """
    Construct a natural-language brief text from search results.

    Args:
        query: The original search query.
        top_results: List of top document texts retrieved.
        scores: Optional list of relevance scores.
        max_results: Maximum number of results to include in the brief.

    Returns:
        A formatted text string suitable for text-to-speech.
    """
    lines = [f"Search results for: {query}"]

    limited_results = top_results[:max_results]
    limited_scores = scores[:max_results] if scores else [None] * max_results

    for i, (doc, score) in enumerate(zip(limited_results, limited_scores), 1):
        if score is not None:
            lines.append(f"Result {i}, relevance {score:.2f}: {doc}")
        else:
            lines.append(f"Result {i}: {doc}")

    lines.append(f"That concludes the summary of the top {len(limited_results)} results.")
    return "\n".join(lines)


def generate_audio_brief(
    text: str,
    voice_id: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> AudioBrief:
    """
    Generate a spoken audio brief from text using ElevenLabs Text-to-Speech.

    ElevenLabs provides high-quality neural text-to-speech synthesis with
    natural-sounding voices suitable for generating spoken search result summaries.

    Args:
        text: The text content to convert to speech.
        voice_id: ElevenLabs voice ID (default: Rachel).
        api_key: ElevenLabs API key (falls back to ELEVENLABS_API_KEY env var).
        model_id: ElevenLabs model ID for synthesis.
        output_format: Output audio format (e.g., mp3_44100_128).

    Returns:
        AudioBrief containing the generated audio bytes.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required for ElevenLabs TTS.")

    vid = voice_id or DEFAULT_VOICE_ID
    url = f"{ELEVENLABS_TTS_URL}/{vid}"

    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    audio_bytes = response.content

    # Rough duration estimate: ~150 words per minute for English
    word_count = len(text.split())
    duration_ms = int((word_count / 150.0) * 60 * 1000)

    return AudioBrief(
        text_content=text,
        voice_id=vid,
        audio_bytes=audio_bytes,
        model_id=model_id,
        duration_estimate_ms=duration_ms,
    )


def generate_retrieval_audio_brief(
    query: str,
    top_results: List[str],
    scores: Optional[List[float]] = None,
    voice_id: Optional[str] = None,
    api_key: Optional[str] = None,
    max_results: int = 3,
) -> AudioBrief:
    """
    Full pipeline: build a brief from search results and generate spoken audio.

    Args:
        query: The original search query.
        top_results: List of top document texts.
        scores: Optional relevance scores.
        voice_id: ElevenLabs voice ID.
        api_key: ElevenLabs API key.
        max_results: Maximum results to include.

    Returns:
        AudioBrief with the generated audio.
    """
    brief_text = build_brief_text(query, top_results, scores, max_results)
    return generate_audio_brief(
        text=brief_text,
        voice_id=voice_id,
        api_key=api_key,
    )


if __name__ == "__main__":
    sample_results = [
        "Neural networks are a class of machine learning models inspired by biological neurons.",
        "Deep learning has transformed computer vision, natural language processing, and speech recognition.",
        "Transformer architectures enable state-of-the-art results across many NLP tasks.",
    ]
    sample_scores = [0.92, 0.85, 0.78]
    audio = generate_retrieval_audio_brief(
        query="latest advances in machine learning",
        top_results=sample_results,
        scores=sample_scores,
        max_results=2,
    )
    print(f"Voice: {audio.voice_id}")
    print(f"Model: {audio.model_id}")
    print(f"Audio size: {len(audio.audio_bytes)} bytes")
    print(f"Estimated duration: {audio.duration_estimate_ms}ms")
    print(f"Text content:\n{audio.text_content}")
