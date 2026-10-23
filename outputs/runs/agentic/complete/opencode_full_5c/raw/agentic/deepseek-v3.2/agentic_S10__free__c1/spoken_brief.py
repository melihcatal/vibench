import os
from typing import Optional
from openai import OpenAI
from model_client import get_client


def generate_spoken_brief(text: str, voice: str = "alloy", speed: float = 1.0) -> bytes:
    """
    Generate a spoken brief from model output using OpenAI's TTS API.

    Args:
        text: Text to convert to speech
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        speed: Speaking speed (0.25 to 4.0)

    Returns:
        Audio data as bytes
    """
    client = get_client()

    # Validate voice parameter
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice not in valid_voices:
        raise ValueError(f"Voice must be one of: {', '.join(valid_voices)}")

    # Validate speed parameter
    if speed < 0.25 or speed > 4.0:
        raise ValueError("Speed must be between 0.25 and 4.0")

    # Truncate text if too long (TTS has token limits)
    max_chars = 4096
    if len(text) > max_chars:
        text = text[:max_chars] + "..."

    try:
        response = client.audio.speech.create(
            model="tts-1", voice=voice, input=text, speed=speed
        )

        # Get audio data as bytes
        audio_data = response.content

        return audio_data

    except Exception as e:
        raise Exception(f"Failed to generate spoken brief: {str(e)}")


def save_spoken_brief(
    text: str, output_path: str, voice: str = "alloy", speed: float = 1.0
) -> None:
    """
    Generate and save spoken brief to file.

    Args:
        text: Text to convert to speech
        output_path: Path to save audio file
        voice: Voice to use
        speed: Speaking speed
    """
    audio_data = generate_spoken_brief(text, voice, speed)

    with open(output_path, "wb") as f:
        f.write(audio_data)


def create_summary_for_speech(text: str, max_length: int = 500) -> str:
    """
    Create a summary optimized for speech synthesis.

    Args:
        text: Original text
        max_length: Maximum characters for speech

    Returns:
        Text optimized for TTS
    """
    from summarize_text import summarize_text

    # First get a summary
    summary = summarize_text(text, max_length // 5)  # Approximate word count

    # Optimize for speech
    import re

    # Remove markdown and special characters
    clean_text = re.sub(r"[#*_`~]", "", summary)

    # Replace abbreviations
    replacements = {
        "e.g.": "for example",
        "i.e.": "that is",
        "etc.": "and so on",
        "vs.": "versus",
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Misses",
        "Ms.": "Miss",
    }

    for abbr, full in replacements.items():
        clean_text = clean_text.replace(abbr, full)

    # Ensure proper spacing
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    # Add natural pauses with commas
    sentences = re.split(r"[.!?]", clean_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Join with appropriate pauses
    speech_text = ", ".join(sentences)

    # Truncate if still too long
    if len(speech_text) > max_length:
        speech_text = speech_text[:max_length]
        # Try to end at a sentence boundary
        last_period = speech_text.rfind(".")
        if last_period > max_length * 0.8:
            speech_text = speech_text[: last_period + 1]
        else:
            speech_text = speech_text.rstrip() + "..."

    return speech_text


def get_available_voices() -> dict:
    """
    Get information about available TTS voices.

    Returns:
        Dictionary with voice information
    """
    return {
        "alloy": {
            "gender": "neutral",
            "accent": "American",
            "description": "Clear and versatile voice",
        },
        "echo": {
            "gender": "male",
            "accent": "American",
            "description": "Warm and friendly voice",
        },
        "fable": {
            "gender": "female",
            "accent": "British",
            "description": "Elegant and articulate voice",
        },
        "onyx": {
            "gender": "male",
            "accent": "American",
            "description": "Deep and resonant voice",
        },
        "nova": {
            "gender": "female",
            "accent": "American",
            "description": "Bright and cheerful voice",
        },
        "shimmer": {
            "gender": "female",
            "accent": "American",
            "description": "Soft and soothing voice",
        },
    }


def text_to_speech_with_fallback(text: str, voice: str = "alloy") -> Optional[bytes]:
    """
    Convert text to speech with fallback options.

    Args:
        text: Text to convert
        voice: Preferred voice

    Returns:
        Audio data or None if failed
    """
    try:
        return generate_spoken_brief(text, voice)
    except Exception as e:
        print(f"TTS failed with voice {voice}: {str(e)}")

        # Try fallback voices
        fallback_voices = ["nova", "echo", "alloy"]
        for fallback_voice in fallback_voices:
            if fallback_voice == voice:
                continue

            try:
                print(f"Trying fallback voice: {fallback_voice}")
                return generate_spoken_brief(text, fallback_voice)
            except Exception:
                continue

        # If all TTS fails, return None
        return None
