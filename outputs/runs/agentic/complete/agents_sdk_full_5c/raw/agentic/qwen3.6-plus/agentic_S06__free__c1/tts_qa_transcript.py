"""
tts_qa_transcript.py - Transcribe synthesized QA samples to verify spoken output using OpenAI Whisper API.

Provider: OpenAI (https://api.openai.com)
Endpoint: POST https://api.openai.com/v1/audio/transcriptions
Model: whisper-1
SDK: openai Python package
"""

from __future__ import annotations

import os
import io
from dataclasses import dataclass
from typing import List, Optional, Union
from pathlib import Path

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_WHISPER_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_WHISPER_MODEL = "whisper-1"

# Supported audio formats for OpenAI Whisper
WHISPER_SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}


@dataclass
class TranscriptResult:
    """Result from Whisper transcription.

    Attributes:
        text: Transcribed text output.
        language: Detected language code.
        model: Whisper model used.
        confidence: Optional confidence score (if available).
    """
    text: str
    language: str = ""
    model: str = OPENAI_WHISPER_MODEL
    confidence: Optional[float] = None


def get_openai_client(
    api_key: Optional[str] = None,
) -> OpenAI:
    """Create an OpenAI API client for Whisper transcription.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set "
            "or an explicit api_key must be provided."
        )
    return OpenAI(api_key=key)


def transcribe_audio_file(
    audio_path: Union[str, Path],
    model: str = OPENAI_WHISPER_MODEL,
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    response_format: str = "text",
    temperature: float = 0.0,
    api_key: Optional[str] = None,
) -> TranscriptResult:
    """Transcribe a synthesized audio file using OpenAI Whisper API.

    Args:
        audio_path: Path to the audio file (mp3, wav, m4a, etc.).
        model: OpenAI Whisper model (default: 'whisper-1').
        language: ISO-639-1 language code (e.g., 'en', 'es'). Auto-detected if None.
        prompt: Optional prompt to guide transcription style.
        response_format: Output format ('text', 'json', 'verbose_json', 'srt', 'vtt').
        temperature: Sampling temperature (0.0 for deterministic).
        api_key: Optional explicit OpenAI API key override.

    Returns:
        TranscriptResult with transcribed text and metadata.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError: If the audio format is unsupported.
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    ext = audio_path.suffix.lower().lstrip(".")
    if ext not in WHISPER_SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {ext}. "
            f"Supported: {', '.join(sorted(WHISPER_SUPPORTED_FORMATS))}"
        )

    client = get_openai_client(api_key=api_key)

    kwargs = {
        "model": model,
        "temperature": temperature,
        "response_format": response_format,
    }
    if language:
        kwargs["language"] = language
    if prompt:
        kwargs["prompt"] = prompt

    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            file=audio_file,
            **kwargs,
        )

    # Whisper returns text string for 'text' format
    if isinstance(response, str):
        text = response
    elif hasattr(response, 'text'):
        text = response.text
    else:
        text = str(response)

    detected_lang = language or ""

    return TranscriptResult(
        text=text.strip(),
        language=detected_lang,
        model=model,
    )


def transcribe_audio_bytes(
    audio_bytes: bytes,
    filename: str = "audio.mp3",
    model: str = OPENAI_WHISPER_MODEL,
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    temperature: float = 0.0,
    api_key: Optional[str] = None,
) -> TranscriptResult:
    """Transcribe audio from in-memory bytes using OpenAI Whisper API.

    Args:
        audio_bytes: Raw audio bytes.
        filename: Filename with extension for format detection.
        model: OpenAI Whisper model.
        language: ISO-639-1 language code.
        prompt: Optional transcription prompt.
        temperature: Sampling temperature.
        api_key: Optional explicit OpenAI API key override.

    Returns:
        TranscriptResult with transcribed text.
    """
    if not audio_bytes:
        raise ValueError("Audio bytes cannot be empty.")

    client = get_openai_client(api_key=api_key)

    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename

    kwargs = {
        "model": model,
        "temperature": temperature,
        "response_format": "text",
    }
    if language:
        kwargs["language"] = language
    if prompt:
        kwargs["prompt"] = prompt

    response = client.audio.transcriptions.create(
        file=audio_file,
        **kwargs,
    )

    if isinstance(response, str):
        text = response
    elif hasattr(response, 'text'):
        text = response.text
    else:
        text = str(response)

    return TranscriptResult(
        text=text.strip(),
        language=language or "",
        model=model,
    )


def verify_tts_output(
    audio_path: Union[str, Path],
    expected_text: str,
    model: str = OPENAI_WHISPER_MODEL,
    api_key: Optional[str] = None,
) -> dict:
    """Verify synthesized speech output against expected text.

    Transcribes the audio and compares against the expected narration
    script to verify TTS accuracy.

    Args:
        audio_path: Path to the synthesized audio file.
        expected_text: The original text that was synthesized.
        model: OpenAI Whisper model.
        api_key: Optional explicit OpenAI API key override.

    Returns:
        Dict with transcript, expected text, match status, and similarity.
    """
    result = transcribe_audio_file(audio_path, model=model, api_key=api_key)

    # Normalize texts for comparison
    transcript_normalized = " ".join(result.text.lower().split())
    expected_normalized = " ".join(expected_text.lower().split())

    # Simple word-level overlap metric
    transcript_words = set(transcript_normalized.split())
    expected_words = set(expected_normalized.split())

    if expected_words:
        word_overlap = len(transcript_words & expected_words) / len(expected_words)
    else:
        word_overlap = 0.0

    return {
        "transcript": result.text,
        "expected": expected_text,
        "match": transcript_normalized == expected_normalized,
        "word_overlap": round(word_overlap, 4),
        "model": model,
        "language": result.language,
    }


def transcribe_batch(
    audio_paths: List[Union[str, Path]],
    model: str = OPENAI_WHISPER_MODEL,
    language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[TranscriptResult]:
    """Transcribe multiple audio files using Whisper.

    Args:
        audio_paths: List of audio file paths.
        model: OpenAI Whisper model.
        language: ISO-639-1 language code.
        api_key: Optional explicit OpenAI API key override.

    Returns:
        List of TranscriptResult objects.
    """
    results = []
    for path in audio_paths:
        result = transcribe_audio_file(
            path, model=model, language=language, api_key=api_key
        )
        results.append(result)
    return results


if __name__ == "__main__":
    from synthesize_text import synthesize_text
    from save_audio import save_audio_to_file

    sample_text = "This is a quality assurance test of the text-to-speech pipeline."
    tts_response = synthesize_text(sample_text)
    audio_path = save_audio_to_file(tts_response, "qa_test.mp3", overwrite=True)

    verification = verify_tts_output(audio_path, sample_text)
    print(f"Transcript: {verification['transcript']}")
    print(f"Expected: {verification['expected']}")
    print(f"Match: {verification['match']}")
    print(f"Word overlap: {verification['word_overlap']}")
