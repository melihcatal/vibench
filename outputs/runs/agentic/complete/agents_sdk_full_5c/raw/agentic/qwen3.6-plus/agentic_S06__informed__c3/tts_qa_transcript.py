"""Transcribe synthesized QA samples to verify spoken output using AssemblyAI.

This module takes synthesized audio files (MP3, WAV, etc.) and transcribes them
using AssemblyAI's Speech-to-Text API to verify the TTS output matches
the original narration script.
"""

import os
import time
from typing import Dict, List, Optional

import assemblyai as aai


def transcribe_qa_sample(
    audio_file_path: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> str:
    """Transcribe a synthesized QA audio sample using AssemblyAI.

    AssemblyAI transcribes the audio to verify the spoken output
    matches the original text. Requires ASSEMBLYAI_API_KEY env var
    if api_key is not provided.

    Args:
        audio_file_path: Path to the local audio file to transcribe.
        api_key: AssemblyAI API key. Falls back to ASSEMBLYAI_API_KEY env var.
        language_code: Language code for transcription (e.g. "en", "es", "fr").

    Returns:
        The transcribed text string from AssemblyAI.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError(
            "AssemblyAI API key required. Set ASSEMBLYAI_API_KEY or pass api_key."
        )

    aai.settings.api_key = key

    config = aai.TranscriptionConfig(
        language_code=language_code,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    return transcript.text


def transcribe_qa_sample_url(
    audio_url: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> str:
    """Transcribe audio from a remote URL using AssemblyAI.

    Args:
        audio_url: Publicly accessible URL to the audio file.
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.

    Returns:
        The transcribed text string.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError(
            "AssemblyAI API key required. Set ASSEMBLYAI_API_KEY or pass api_key."
        )

    aai.settings.api_key = key

    config = aai.TranscriptionConfig(
        language_code=language_code,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    return transcript.text


def verify_tts_output(
    original_text: str,
    audio_file_path: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
    similarity_threshold: float = 0.8,
) -> Dict:
    """Verify TTS output by transcribing audio and comparing to original text.

    Uses AssemblyAI to transcribe the audio, then computes a rough
    similarity score against the original narration script.

    Args:
        original_text: The text that was originally sent to TTS.
        audio_file_path: Path to the synthesized audio file.
        api_key: AssemblyAI API key.
        language_code: Transcription language code.
        similarity_threshold: Minimum word overlap ratio to pass QA.

    Returns:
        Dict with 'transcribed_text', 'original_text', 'passed', 'similarity_score'.
    """
    transcribed = transcribe_qa_sample(
        audio_file_path=audio_file_path,
        api_key=api_key,
        language_code=language_code,
    )

    original_words = set(original_text.lower().split())
    transcribed_words = set(transcribed.lower().split())

    if not original_words:
        similarity = 0.0
    else:
        overlap = original_words & transcribed_words
        similarity = len(overlap) / len(original_words)

    return {
        "transcribed_text": transcribed,
        "original_text": original_text,
        "passed": similarity >= similarity_threshold,
        "similarity_score": similarity,
        "provider": "assemblyai",
    }


def transcribe_qa_batch(
    audio_file_paths: List[str],
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> List[str]:
    """Transcribe multiple QA audio samples using AssemblyAI.

    Args:
        audio_file_paths: List of local audio file paths to transcribe.
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.

    Returns:
        List of transcribed text strings, one per audio file.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError(
            "AssemblyAI API key required. Set ASSEMBLYAI_API_KEY or pass api_key."
        )

    aai.settings.api_key = key

    config = aai.TranscriptionConfig(
        language_code=language_code,
    )

    transcriber = aai.Transcriber()
    results = []

    for path in audio_file_paths:
        transcript = transcriber.transcribe(path, config=config)
        if transcript.status == aai.TranscriptStatus.error:
            results.append(f"[ERROR: {transcript.error}]")
        else:
            results.append(transcript.text)

    return results
