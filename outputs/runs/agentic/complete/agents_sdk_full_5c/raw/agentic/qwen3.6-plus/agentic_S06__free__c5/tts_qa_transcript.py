"""Transcribe synthesized QA samples to verify spoken output using OpenAI Whisper API."""

import os
from typing import Optional

from openai import OpenAI


def transcribe_qa_audio(
    audio_path: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "text",
    prompt: Optional[str] = None,
) -> str:
    """Transcribe synthesized QA audio using OpenAI Whisper API.

    Uploads the audio file to api.openai.com and transcribes it using the
    Whisper model "whisper-1" to verify the spoken output matches the
    original narration script.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    with open(audio_path, "rb") as audio_file:
        kwargs = {
            "file": audio_file,
            "model": model,
            "response_format": response_format,
        }
        if language:
            kwargs["language"] = language
        if prompt:
            kwargs["prompt"] = prompt

        transcription = client.audio.transcriptions.create(**kwargs)

    if response_format == "text":
        return transcription
    return transcription.text


def verify_tts_output(
    audio_path: str,
    expected_text: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    similarity_threshold: float = 0.8,
) -> dict:
    """Transcribe audio and compare against expected text to verify TTS output.

    Uses OpenAI Whisper via api.openai.com with the "whisper-1" model to
    transcribe the synthesized audio, then computes a word-level similarity
    score against the original expected text.
    """
    transcribed = transcribe_qa_audio(
        audio_path=audio_path,
        model=model,
        language=language,
        response_format="text",
    )

    similarity = _text_similarity(expected_text, transcribed)
    passed = similarity >= similarity_threshold

    return {
        "expected": expected_text,
        "transcribed": transcribed,
        "similarity": similarity,
        "threshold": similarity_threshold,
        "passed": passed,
        "model": model,
    }


def verify_tts_batch(
    audio_text_pairs: list,
    model: str = "whisper-1",
    language: Optional[str] = None,
    similarity_threshold: float = 0.8,
) -> list:
    """Verify multiple TTS outputs by transcribing each and comparing.

    Processes each (audio_path, expected_text) pair through the OpenAI
    Whisper API at api.openai.com using the "whisper-1" model.
    """
    results = []
    for audio_path, expected_text in audio_text_pairs:
        result = verify_tts_output(
            audio_path=audio_path,
            expected_text=expected_text,
            model=model,
            language=language,
            similarity_threshold=similarity_threshold,
        )
        results.append(result)
    return results


def _text_similarity(expected: str, actual: str) -> float:
    """Compute a simple word-level Jaccard similarity between two texts."""
    expected_words = set(expected.lower().split())
    actual_words = set(actual.lower().split())

    if not expected_words and not actual_words:
        return 1.0
    if not expected_words or not actual_words:
        return 0.0

    intersection = expected_words & actual_words
    union = expected_words | actual_words
    return len(intersection) / len(union)
