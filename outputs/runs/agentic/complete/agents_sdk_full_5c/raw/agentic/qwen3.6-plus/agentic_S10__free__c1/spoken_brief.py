"""
spoken_brief.py — Generate a spoken brief from the model output.

Uses the OpenAI Audio/Speech API (api.openai.com) with the
tts-1 model to convert text output into spoken audio (MP3 format).
"""

from __future__ import annotations

import base64
from typing import Optional

from model_client import generate_speech, resolve_model
from model_models import SpeechRequest

# Concrete OpenAI model identifier for text-to-speech
TTS_MODEL = resolve_model("tts-1")  # tts-1

# Available OpenAI TTS voices
OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
DEFAULT_VOICE = "alloy"


def generate_spoken_brief(
    text: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    speed: float = 1.0,
    response_format: str = "mp3",
) -> bytes:
    """
    Convert model output text into spoken audio using the OpenAI
    tts-1 text-to-speech model via api.openai.com.

    Parameters
    ----------
    text : str
        The text to convert to speech.
    voice : str, optional
        OpenAI TTS voice name (alloy, echo, fable, onyx, nova, shimmer).
        Defaults to "alloy".
    model : str, optional
        Concrete OpenAI TTS model ID (defaults to tts-1).
    speed : float
        Playback speed (0.25 to 4.0). Defaults to 1.0.
    response_format : str
        Output audio format (mp3, opus, aac, flac, wav, pcm). Defaults to "mp3".

    Returns
    -------
    bytes
        Raw audio data in the specified format.
    """
    target_model = model or TTS_MODEL
    target_voice = voice or DEFAULT_VOICE

    request = SpeechRequest(
        input_text=text,
        model=target_model,
        voice=target_voice,
        response_format=response_format,
        speed=speed,
    )
    return generate_speech(request)


def generate_spoken_brief_base64(
    text: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    speed: float = 1.0,
    response_format: str = "mp3",
) -> str:
    """
    Convert model output text to spoken audio and return as base64 string.

    Useful for embedding audio in JSON responses or HTML data URIs.

    Parameters
    ----------
    text : str
        The text to convert to speech.
    voice : str, optional
        OpenAI TTS voice name. Defaults to "alloy".
    model : str, optional
        Concrete OpenAI TTS model ID.
    speed : float
        Playback speed. Defaults to 1.0.
    response_format : str
        Output audio format. Defaults to "mp3".

    Returns
    -------
    str
        Base64-encoded audio data.
    """
    audio_bytes = generate_spoken_brief(
        text, voice=voice, model=model, speed=speed, response_format=response_format
    )
    return base64.b64encode(audio_bytes).decode("utf-8")


def create_brief_from_output(
    model_output: str,
    summary_length: str = "brief",
    voice: Optional[str] = None,
    model: Optional[str] = None,
    speed: float = 1.0,
) -> bytes:
    """
    Create a spoken brief from a longer model output by optionally
    truncating or keeping the full text.

    Parameters
    ----------
    model_output : str
        Full model-generated text.
    summary_length : str
        One of "brief" (~150 words), "short" (~300 words), or "full".
    voice : str, optional
        OpenAI TTS voice name.
    model : str, optional
        Concrete OpenAI TTS model ID.
    speed : float
        Playback speed.

    Returns
    -------
    bytes
        Raw audio data.
    """
    words = model_output.split()
    word_limit = {"brief": 150, "short": 300}.get(summary_length, len(words))
    trimmed = " ".join(words[:word_limit])

    return generate_spoken_brief(
        trimmed, voice=voice, model=model, speed=speed
    )


def save_spoken_brief(
    text: str,
    output_path: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    speed: float = 1.0,
    response_format: str = "mp3",
) -> str:
    """
    Generate spoken audio and save it to a file.

    Parameters
    ----------
    text : str
        The text to convert to speech.
    output_path : str
        File path for the output audio file.
    voice : str, optional
        OpenAI TTS voice name.
    model : str, optional
        Concrete OpenAI TTS model ID.
    speed : float
        Playback speed.
    response_format : str
        Output audio format.

    Returns
    -------
    str
        The output file path.
    """
    audio_bytes = generate_spoken_brief(
        text, voice=voice, model=model, speed=speed, response_format=response_format
    )
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


if __name__ == "__main__":
    sample_text = (
        "Welcome to today's briefing. Our analysis shows that renewable energy "
        "adoption increased by 15 percent this quarter, driven primarily by solar "
        "and wind investments in emerging markets."
    )
    print(f"Generating spoken brief using OpenAI {TTS_MODEL}...")
    audio = generate_spoken_brief(sample_text, voice="nova", speed=1.0)
    print(f"Audio generated: {len(audio)} bytes")
