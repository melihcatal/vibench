"""
retrieval_audio_brief.py - Generate a spoken brief from retrieved search results.

Provider: ElevenLabs Text to Speech API
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
Model: eleven_multilingual_v2
"""

import os
from dataclasses import dataclass
from typing import Any

from elevenlabs import ElevenLabs, Voice


ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"

_api_key = os.environ.get("ELEVENLABS_API_KEY", "")


@dataclass
class AudioBriefResult:
    """Result from generating a spoken audio brief."""

    audio_bytes: bytes
    content_type: str
    text_used: str
    model_id: str
    voice_id: str


def _get_elevenlabs_client() -> ElevenLabs:
    if not _api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    return ElevenLabs(api_key=_api_key)


def _build_brief_script(
    query: str,
    results: list[str],
    max_results: int = 5,
) -> str:
    """Compose a natural-language brief script from search results.

    Args:
        query: The original search query.
        results: List of retrieved document texts.
        max_results: Maximum number of results to include.

    Returns:
        A script string suitable for text-to-speech synthesis.
    """
    limited = results[:max_results]
    lines = [f"Here are the top results for: {query}\n"]
    for i, doc in enumerate(limited, start=1):
        # Truncate very long documents for speech
        truncated = doc[:300] + "..." if len(doc) > 300 else doc
        lines.append(f"Result {i}: {truncated}")
    lines.append("\nEnd of results.")
    return "\n\n".join(lines)


def generate_audio_brief(
    query: str,
    results: list[str],
    voice_id: str = ELEVENLABS_VOICE_ID,
    model_id: str = ELEVENLABS_MODEL_ID,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> AudioBriefResult:
    """Generate a spoken audio brief from retrieval search results via ElevenLabs TTS.

    Uses the ElevenLabs API with the eleven_multilingual_v2 model to synthesize
    a natural-sounding spoken summary of search results.

    Args:
        query: The original search query.
        results: List of retrieved document strings.
        voice_id: ElevenLabs voice identifier (default: Rachel).
        model_id: ElevenLabs TTS model (default: eleven_multilingual_v2).
        stability: Voice stability setting (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).

    Returns:
        AudioBriefResult containing the synthesized audio bytes.
    """
    client = _get_elevenlabs_client()
    script = _build_brief_script(query, results)

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=script,
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    )

    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk

    return AudioBriefResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        text_used=script,
        model_id=model_id,
        voice_id=voice_id,
    )


def generate_audio_brief_from_search(
    query: str,
    search_results: list[dict[str, str]],
    voice_id: str = ELEVENLABS_VOICE_ID,
) -> AudioBriefResult:
    """Convenience wrapper that extracts document text from search result dicts.

    Args:
        query: Original search query.
        search_results: List of dicts with a 'document' or 'text' key.
        voice_id: ElevenLabs voice identifier.

    Returns:
        AudioBriefResult with synthesized audio.
    """
    texts: list[str] = []
    for item in search_results:
        doc = item.get("document") or item.get("text") or ""
        texts.append(doc)
    return generate_audio_brief(query, texts, voice_id=voice_id)


def main() -> None:
    query = "latest advances in large language models"
    results = [
        "Recent transformer architectures have improved reasoning capabilities significantly.",
        "Multimodal models now combine text, image, and audio understanding.",
        "Open-weight models are enabling broader access to state-of-the-art AI.",
    ]
    brief = generate_audio_brief(query, results)
    print(f"Model: {brief.model_id}")
    print(f"Voice: {brief.voice_id}")
    print(f"Audio size: {len(brief.audio_bytes)} bytes")
    print(f"Content type: {brief.content_type}")


if __name__ == "__main__":
    main()
