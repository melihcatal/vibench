"""
Generate a spoken brief from retrieved search results using ElevenLabs Text-to-Speech.

Converts search result summaries into natural-sounding speech using
the ElevenLabs TTS API with the elevenlabs SDK.

Requires ELEVENLABS_API_KEY environment variable or explicit api_key parameter.
"""

import os
from typing import List, Optional

from elevenlabs import ElevenLabs, Voice, VoiceSettings

ELEVENLABS_DEFAULT_VOICE = "Rachel"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"
ELEVENLABS_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    """
    Create and return an authenticated ElevenLabs client.

    Args:
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.

    Returns:
        Configured elevenlabs.ElevenLabs instance.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ElevenLabs API key not provided and ELEVENLABS_API_KEY not set")
    return ElevenLabs(api_key=key)


def _format_search_brief(
    query: str,
    results: List[dict],
    top_k: int = 3,
) -> str:
    """
    Format search results into a spoken brief script.

    Args:
        query: The original search query.
        results: List of dicts with 'document' and 'score' keys.
        top_k: Number of top results to include.

    Returns:
        Natural language brief script for text-to-speech.
    """
    top_results = results[:top_k]
    if not top_results:
        return f"No results found for your query: {query}"

    script_parts = [f"Here are the top results for: {query}."]

    for i, result in enumerate(top_results, 1):
        doc_text = result.get("document", "")
        score = result.get("score", 0.0)
        truncated = doc_text[:300] + ("..." if len(doc_text) > 300 else "")
        script_parts.append(
            f"Result {i}, with a relevance score of {score:.2f}: {truncated}"
        )

    script_parts.append("End of results.")
    return " ".join(script_parts)


def generate_audio_brief(
    query: str,
    results: List[dict],
    api_key: Optional[str] = None,
    voice_name: str = ELEVENLABS_DEFAULT_VOICE,
    voice_id: str = ELEVENLABS_DEFAULT_VOICE_ID,
    model: str = ELEVENLABS_DEFAULT_MODEL,
    client: Optional[ElevenLabs] = None,
    top_k: int = 3,
) -> bytes:
    """
    Generate a spoken audio brief from search results via ElevenLabs TTS.

    Args:
        query: The original search query.
        results: List of search result dicts with 'document' and 'score'.
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.
        voice_name: Human-readable voice name (informational).
        voice_id: ElevenLabs voice ID to use for synthesis.
        model: ElevenLabs TTS model, default eleven_multilingual_v2.
        client: Pre-configured ElevenLabs client (optional).
        top_k: Number of results to include in the brief.

    Returns:
        Audio bytes (MP3 format) of the spoken brief.
    """
    if client is None:
        client = get_elevenlabs_client(api_key)

    script = _format_search_brief(query, results, top_k=top_k)

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model,
        text=script,
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
        ),
    )

    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk

    return audio_bytes


def generate_audio_brief_from_search_results(
    query: str,
    search_results: List[dict],
    api_key: Optional[str] = None,
    voice_id: str = ELEVENLABS_DEFAULT_VOICE_ID,
    model: str = ELEVENLABS_DEFAULT_MODEL,
    top_k: int = 3,
) -> bytes:
    """
    Convenience wrapper to generate audio from search result objects.

    Args:
        query: Search query text.
        search_results: List of SearchResult-like objects with document and score.
        api_key: ElevenLabs API key.
        voice_id: ElevenLabs voice ID.
        model: TTS model identifier.
        top_k: Results to include.

    Returns:
        MP3 audio bytes.
    """
    formatted = []
    for r in search_results:
        doc = getattr(r, "document", None) or r.get("document", "")
        score = getattr(r, "score", None) or r.get("score", 0.0)
        formatted.append({"document": doc, "score": score})

    return generate_audio_brief(
        query=query,
        results=formatted,
        api_key=api_key,
        voice_id=voice_id,
        model=model,
        top_k=top_k,
    )
