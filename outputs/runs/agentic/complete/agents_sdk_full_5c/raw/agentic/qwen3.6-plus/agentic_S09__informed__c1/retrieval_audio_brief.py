"""Generate a spoken brief from retrieved search results using ElevenLabs TTS.

First uses OpenAI GPT-4o-mini to compose a concise spoken brief from search
results, then converts it to speech via the ElevenLabs Text-to-Speech API.
"""

import os
from typing import List, Dict, Optional, Tuple

from openai import OpenAI
import requests


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"


def get_openai_client() -> OpenAI:
    """Create an OpenAI client for brief composition."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def compose_spoken_brief(
    query: str,
    results: List[Dict[str, str]],
    max_words: int = 150,
    model: str = "gpt-4o-mini",
) -> str:
    """Compose a concise spoken brief from search results using OpenAI GPT-4o-mini.

    Args:
        query: The original search query.
        results: List of result dicts with 'text' and 'score' keys.
        max_words: Maximum word count for the spoken brief.
        model: OpenAI chat model ID (defaults to gpt-4o-mini).

    Returns:
        Natural-language spoken brief text optimized for text-to-speech.
    """
    client = get_openai_client()

    results_text = "\n".join(
        f"- {r['text'][:200]} (relevance: {r.get('score', 'N/A')})"
        for r in results[:5]
    )

    system_prompt = (
        "You are a voice assistant. Write a concise spoken brief that summarizes "
        f"search results for a query. Keep it under {max_words} words. Use natural, "
        "conversational language suitable for text-to-speech. Do not use special "
        "characters, URLs, or formatting. Spell out numbers and abbreviations."
    )

    user_prompt = f"Query: {query}\n\nSearch results:\n{results_text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


def generate_audio_brief(
    spoken_brief_text: str,
    api_key: Optional[str] = None,
    voice_id: str = ELEVENLABS_DEFAULT_VOICE_ID,
    model_id: str = "eleven_monolingual_v1",
    output_path: str = "audio_brief.mp3",
) -> str:
    """Generate an audio file from the spoken brief via ElevenLabs TTS API.

    Args:
        spoken_brief_text: Text to convert to speech.
        api_key: ElevenLabs API key (falls back to ELEVENLABS_API_KEY env var).
        voice_id: ElevenLabs voice ID to use.
        model_id: ElevenLabs TTS model ID (e.g., eleven_monolingual_v1, eleven_multilingual_v2).
        output_path: Path to save the generated audio file.

    Returns:
        Path to the generated audio file.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key,
    }

    payload = {
        "text": spoken_brief_text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_brief_from_search_results(
    query: str,
    results: List[Dict[str, str]],
    api_key: Optional[str] = None,
    voice_id: str = ELEVENLABS_DEFAULT_VOICE_ID,
    model_id: str = "eleven_monolingual_v1",
    output_path: str = "audio_brief.mp3",
) -> Tuple[str, str]:
    """Full pipeline: compose brief from results, then generate audio via ElevenLabs.

    Args:
        query: Original search query.
        results: Search result dicts with 'text' and 'score'.
        api_key: ElevenLabs API key.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs TTS model.
        output_path: Output audio file path.

    Returns:
        Tuple of (spoken_brief_text, audio_file_path).
    """
    spoken_brief = compose_spoken_brief(query, results)
    audio_path = generate_audio_brief(
        spoken_brief,
        api_key=api_key,
        voice_id=voice_id,
        model_id=model_id,
        output_path=output_path,
    )
    return spoken_brief, audio_path


def main():
    sample_query = "machine learning fundamentals"
    sample_results = [
        {"text": "Machine learning is a subset of AI that enables systems to learn from data.", "score": 0.92},
        {"text": "Supervised learning uses labeled training data to predict outcomes.", "score": 0.85},
        {"text": "Neural networks are inspired by biological brain structures.", "score": 0.78},
    ]

    try:
        brief, audio_path = generate_brief_from_search_results(
            sample_query, sample_results,
            output_path="brief_demo.mp3",
        )
        print(f"Spoken brief (ElevenLabs):\n{brief}")
        print(f"\nAudio saved to: {audio_path}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set ELEVENLABS_API_KEY and OPENAI_API_KEY to use this module.")


if __name__ == "__main__":
    main()
