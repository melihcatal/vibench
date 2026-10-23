"""
[LATER-STEP] Generate a spoken brief from retrieved search results.
Provider: OpenAI Text-to-Speech API (api.openai.com, model tts-1).
"""

from __future__ import annotations

import os

from openai import OpenAI

from embeddings_client import get_openai_client


def generate_spoken_brief(
    search_results: list[dict],
    query: str,
    output_path: str | None = None,
    voice: str = "alloy",
    api_key: str | None = None,
    client: OpenAI | None = None,
) -> bytes:
    """
    Generate a spoken audio brief summarizing retrieved search results
    using the OpenAI Text-to-Speech API (api.openai.com, model tts-1).

    Args:
        search_results: List of dicts with 'text' and 'score' keys.
        query: The original search query.
        output_path: Optional file path to save the audio.
        voice: OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer).
        api_key: OpenAI API key.
        client: Optional pre-configured OpenAI client.

    Returns:
        Audio data as bytes (MP3 format from OpenAI tts-1 model).
    """
    if client is None:
        client = get_openai_client(api_key=api_key)

    summary_text = _build_brief_text(query, search_results)

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=summary_text,
        response_format="mp3",
    )

    audio_bytes = response.content

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return audio_bytes


def _build_brief_text(query: str, results: list[dict]) -> str:
    """Build a natural-language brief from search results for TTS."""
    lines = [f"Here are the search results for: {query}"]

    for i, result in enumerate(results, start=1):
        text = result.get("text", "")
        score = result.get("score", 0.0)
        lines.append(f"Result {i}: {text} (relevance score: {score:.2f})")

    if not results:
        lines.append("No relevant results were found.")

    return " ".join(lines)


def brief_to_file(
    search_results: list[dict],
    query: str,
    output_path: str,
    voice: str = "alloy",
    api_key: str | None = None,
) -> str:
    """
    Generate a spoken audio brief and save it to a file.
    Uses the OpenAI Text-to-Speech API (api.openai.com, model tts-1).

    Args:
        search_results: List of result dicts with 'text' and 'score'.
        query: The original search query.
        output_path: Path to save the MP3 file.
        voice: OpenAI TTS voice selection.
        api_key: OpenAI API key.

    Returns:
        The output file path.
    """
    generate_spoken_brief(
        search_results=search_results,
        query=query,
        output_path=output_path,
        voice=voice,
        api_key=api_key,
    )
    return output_path


if __name__ == "__main__":
    sample_results = [
        {"text": "Mount Everest is the highest mountain above sea level.", "score": 0.92},
        {"text": "The tallest mountain from base to peak is Mauna Kea in Hawaii.", "score": 0.85},
        {"text": "K2 is the second highest mountain in the world.", "score": 0.78},
    ]

    output_file = "search_brief.mp3"
    path = brief_to_file(sample_results, "What is the tallest mountain?", output_file)
    print(f"Audio brief saved to: {path}")
