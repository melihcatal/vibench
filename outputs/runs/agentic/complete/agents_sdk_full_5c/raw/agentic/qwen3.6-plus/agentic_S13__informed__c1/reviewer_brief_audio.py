"""
[LATER-STEP] reviewer_brief_audio.py - Generate spoken briefs for
moderation reviewers using ElevenLabs Text-to-Speech API.

Provider: ElevenLabs
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

import os
from typing import Optional

from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient

ELEVENLABS_DEFAULT_VOICE = "Rachel"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"


def generate_reviewer_brief_audio(
    brief_text: str,
    voice: str = ELEVENLABS_DEFAULT_VOICE,
    model: str = ELEVENLABS_DEFAULT_MODEL,
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> dict:
    """
    Generate a spoken audio brief for a moderation reviewer using
    ElevenLabs Text-to-Speech API (eleven_multilingual_v2 model).

    Args:
        brief_text: The text content of the moderation brief.
        voice: ElevenLabs voice name or ID.
        model: ElevenLabs TTS model identifier.
        api_key: Optional ElevenLabs API key override.
        output_path: Optional file path to save the audio.

    Returns:
        Dict with 'audio_bytes', 'voice', 'model', 'text_length'.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    client = ElevenLabs(api_key=key)

    audio_generator = client.text_to_speech.convert(
        voice=voice,
        model_id=model,
        text=brief_text,
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return {
        "audio_bytes": audio_bytes,
        "voice": voice,
        "model": model,
        "text_length": len(brief_text),
        "output_path": output_path,
    }


def generate_reviewer_briefs_batch(
    briefs: list[dict],
    voice: str = ELEVENLABS_DEFAULT_VOICE,
    model: str = ELEVENLABS_DEFAULT_MODEL,
    api_key: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> list[dict]:
    """
    Generate audio briefs for multiple moderation review cases using
    ElevenLabs TTS API.

    Args:
        briefs: List of dicts, each with 'id' and 'text' keys.
        voice: ElevenLabs voice name or ID.
        model: ElevenLabs TTS model identifier.
        api_key: Optional ElevenLabs API key override.
        output_dir: Optional directory to save audio files.

    Returns:
        List of result dicts with audio metadata for each brief.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    client = ElevenLabs(api_key=key)

    results = []
    for brief in briefs:
        brief_id = brief.get("id", "unknown")
        text = brief.get("text", "")
        output_path = None
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"brief_{brief_id}.mp3")

        audio_generator = client.text_to_speech.convert(
            voice=voice,
            model_id=model,
            text=text,
        )

        audio_bytes = b""
        for chunk in audio_generator:
            audio_bytes += chunk

        if output_path:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        results.append({
            "id": brief_id,
            "audio_bytes": audio_bytes,
            "voice": voice,
            "model": model,
            "text_length": len(text),
            "output_path": output_path,
        })

    return results


if __name__ == "__main__":
    sample_brief = (
        "Moderation case 42 has been flagged for review. "
        "The content was scored with a violence severity of 6 out of 7. "
        "Please evaluate the decision and provide feedback."
    )
    result = generate_reviewer_brief_audio(sample_brief)
    print(f"Audio generated: {result['text_length']} chars, model: {result['model']}")
