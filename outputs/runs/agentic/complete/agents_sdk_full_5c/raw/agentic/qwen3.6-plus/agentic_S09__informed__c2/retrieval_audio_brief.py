"""
Later-step: Generate a spoken brief from retrieved search results.
Provider: ElevenLabs Text-to-Speech via elevenlabs SDK / REST.
Auth: ELEVENLABS_API_KEY
Model: eleven_multilingual_v2 (voice: Rachel / default)
"""

import os
from typing import List, Optional

from elevenlabs import ElevenLabs, Voice, VoiceSettings


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    """Create an ElevenLabs client."""
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return ElevenLabs(api_key=key)


def format_search_results_for_brief(
    query: str,
    results: List[dict],
    max_results: int = 5,
) -> str:
    """Format search results into a natural-language brief script."""
    lines = [f"Here are the results for your query: {query}\n"]

    for i, result in enumerate(results[:max_results], start=1):
        text = result.get("text", result.get("content", ""))
        score = result.get("score", result.get("similarity", ""))
        title = result.get("title", result.get("source", f"Result {i}"))
        lines.append(f"Result {i} from {title} (relevance score: {score}):")
        lines.append(text)
        lines.append("")

    lines.append("End of results.")
    return "\n".join(lines)


def generate_audio_brief(
    query: str,
    results: List[dict],
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    voice_name: str = "Rachel",
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    api_key: Optional[str] = None,
) -> bytes:
    """Generate a spoken audio brief from retrieved search results using ElevenLabs.

    Uses the eleven_multilingual_v2 model for multilingual text-to-speech.

    Args:
        query: The original search query.
        results: List of search result dicts with 'text', 'score', etc.
        voice_id: ElevenLabs voice ID (default: Rachel).
        voice_name: Human-readable voice name.
        model_id: ElevenLabs TTS model identifier.
        stability: Voice stability (0.0-1.0).
        similarity_boost: Voice similarity boost (0.0-1.0).
        api_key: Optional override for ELEVENLABS_API_KEY.

    Returns:
        Audio bytes (MP3 format).
    """
    client = get_elevenlabs_client(api_key=api_key)

    script = format_search_results_for_brief(query, results)

    voice = Voice(
        voice_id=voice_id,
        name=voice_name,
        settings=VoiceSettings(
            stability=stability,
            similarity_boost=similarity_boost,
        ),
    )

    audio = client.generate(
        text=script,
        voice=voice,
        model=model_id,
    )

    # Collect audio bytes
    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk

    return audio_bytes


def save_audio_brief(
    query: str,
    results: List[dict],
    output_path: str = "search_brief.mp3",
    **kwargs,
) -> str:
    """Generate and save an audio brief to a file."""
    audio_bytes = generate_audio_brief(query, results, **kwargs)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


if __name__ == "__main__":
    sample_results = [
        {"text": "Vector embeddings represent text as dense numerical arrays.", "score": 0.92, "title": "ML Glossary"},
        {"text": "Semantic search uses cosine similarity over embeddings.", "score": 0.88, "title": "AI Handbook"},
    ]
    # Requires ELEVENLABS_API_KEY
    # path = save_audio_brief("What are embeddings?", sample_results)
    # print(f"Audio saved to: {path}")
    print("Configure ELEVENLABS_API_KEY to run.")
