import os
from typing import Optional
from openai import OpenAI
from elevenlabs import ElevenLabs
from model_client import get_llm_client


def generate_spoken_brief(text: str, voice: Optional[str] = None) -> dict:
    """
    Generate a spoken brief from model output using ElevenLabs text-to-speech.

    Args:
        text: Text to convert to speech
        voice: Optional voice ID to use

    Returns:
        Dictionary with audio metadata
    """
    # First, create a concise spoken version using OpenAI
    client = get_llm_client()

    try:
        # Create a spoken-friendly version
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Convert this text into a natural, spoken brief suitable for audio playback. Keep it conversational and concise.",
                },
                {"role": "user", "content": text},
            ],
            max_tokens=300,
            temperature=0.5,
        )

        spoken_text = response.choices[0].message.content.strip()

        # Now convert to speech using ElevenLabs
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")

        elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)

        voice_to_use = voice or "Rachel"

        # Generate audio
        audio = elevenlabs_client.generate(
            text=spoken_text, voice=voice_to_use, model="eleven_monolingual_v1"
        )

        # Save audio to file
        import uuid

        filename = f"spoken_brief_{uuid.uuid4().hex[:8]}.mp3"

        with open(filename, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return {
            "original_text": text,
            "spoken_text": spoken_text,
            "audio_file": filename,
            "voice_used": voice_to_use,
            "tts_provider": "elevenlabs",
            "tts_model": "eleven_monolingual_v1",
            "llm_model": "gpt-4o-mini",
            "llm_provider": "openai",
        }

    except Exception as e:
        raise Exception(f"Failed to generate spoken brief: {str(e)}")


def create_executive_summary_audio(
    text: str, duration_limit: Optional[int] = None
) -> dict:
    """
    Create an executive summary audio from model output.

    Args:
        text: Text to summarize and convert to audio
        duration_limit: Optional maximum duration in seconds

    Returns:
        Dictionary with audio summary metadata
    """
    client = get_llm_client()

    try:
        # Create executive summary
        prompt = f"Create a concise executive summary suitable for a 1-2 minute audio briefing:\n\n{text}"

        if duration_limit:
            prompt += (
                f"\n\nKeep the summary under {duration_limit} seconds when spoken."
            )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You create professional executive summaries for audio presentations.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.4,
        )

        summary = response.choices[0].message.content.strip()

        # Convert to speech
        return generate_spoken_brief(summary, voice="Antoni")

    except Exception as e:
        raise Exception(f"Failed to create executive summary audio: {str(e)}")


def estimate_speech_duration(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate speech duration for text.

    Args:
        text: Text to estimate duration for
        words_per_minute: Average speaking rate

    Returns:
        Estimated duration in seconds
    """
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    return minutes * 60


def get_available_voices() -> list:
    """
    Get available voices from ElevenLabs.

    Returns:
        List of available voice names
    """
    try:
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            return []

        elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        voices = elevenlabs_client.voices.get_all()

        return [voice.name for voice in voices.voices]

    except Exception:
        # Fallback to default voices
        return ["Rachel", "Antoni", "Bella", "Josh", "Elli", "Callum"]


def optimize_for_speech(text: str) -> str:
    """
    Optimize text for speech synthesis.

    Args:
        text: Text to optimize

    Returns:
        Speech-optimized text
    """
    client = get_llm_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Optimize this text for speech synthesis. Make it more natural for spoken delivery, add appropriate pauses, and simplify complex sentences.",
                },
                {"role": "user", "content": text},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        optimized = response.choices[0].message.content.strip()

        return optimized

    except Exception as e:
        # Fallback to original text
        return text
