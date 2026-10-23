"""
[LATER-STEP] reviewer_brief_audio.py
Generate spoken briefs for moderation reviewers.
Uses the OpenAI Text-to-Speech API (openai SDK, tts-1-hd model).
"""

import base64
import os
from typing import Optional

from openai import OpenAI

from safety_client import get_openai_client
from safety_models import ModerationResponse, BatchModerationResponse


OPENAI_TTS_MODEL = "tts-1-hd"
OPENAI_TTS_VOICE = "nova"
OPENAI_SPEECH_FORMAT = "mp3"


def generate_reviewer_brief_audio(
    case_summary: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
    voice: str = OPENAI_TTS_VOICE,
    response_format: str = OPENAI_SPEECH_FORMAT,
) -> bytes:
    """
    Generate a spoken audio brief for a moderation reviewer using OpenAI TTS.

    Args:
        case_summary: Text summary of the moderation case to be spoken.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI TTS model identifier (default: tts-1-hd).
        voice: OpenAI TTS voice name (default: nova).
        response_format: Audio format (default: mp3).

    Returns:
        Raw audio bytes in the requested format.
    """
    client = get_openai_client(api_key=api_key)

    speech_response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=case_summary,
        response_format=response_format,
    )

    return speech_response.content


def generate_reviewer_brief_audio_base64(
    case_summary: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
    voice: str = OPENAI_TTS_VOICE,
    response_format: str = OPENAI_SPEECH_FORMAT,
) -> str:
    """
    Generate a spoken audio brief and return as base64-encoded string.

    Args:
        case_summary: Text summary of the moderation case to be spoken.
        api_key: Optional OpenAI API key.
        model: OpenAI TTS model identifier (default: tts-1-hd).
        voice: OpenAI TTS voice name (default: nova).
        response_format: Audio format (default: mp3).

    Returns:
        Base64-encoded audio string.
    """
    audio_bytes = generate_reviewer_brief_audio(
        case_summary,
        api_key=api_key,
        model=model,
        voice=voice,
        response_format=response_format,
    )
    return base64.b64encode(audio_bytes).decode("utf-8")


def save_reviewer_brief_audio(
    case_summary: str,
    output_path: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
    voice: str = OPENAI_TTS_VOICE,
    response_format: str = OPENAI_SPEECH_FORMAT,
) -> str:
    """
    Generate and save a spoken audio brief to a file.

    Args:
        case_summary: Text summary of the moderation case to be spoken.
        output_path: File path to save the audio.
        api_key: Optional OpenAI API key.
        model: OpenAI TTS model identifier (default: tts-1-hd).
        voice: OpenAI TTS voice name (default: nova).
        response_format: Audio format (default: mp3).

    Returns:
        The output_path where the audio was saved.
    """
    audio_bytes = generate_reviewer_brief_audio(
        case_summary,
        api_key=api_key,
        model=model,
        voice=voice,
        response_format=response_format,
    )
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def generate_batch_reviewer_briefs(
    batch_response: BatchModerationResponse,
    texts: list[str],
    output_dir: str = "./reviewer_briefs",
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
    voice: str = OPENAI_TTS_VOICE,
    response_format: str = OPENAI_SPEECH_FORMAT,
) -> list[str]:
    """
    Generate spoken audio briefs for all flagged cases in a batch.

    Args:
        batch_response: BatchModerationResponse from moderation.
        texts: Original list of texts corresponding to the batch.
        output_dir: Directory to save audio files.
        api_key: Optional OpenAI API key.
        model: OpenAI TTS model identifier (default: tts-1-hd).
        voice: OpenAI TTS voice name (default: nova).
        response_format: Audio format (default: mp3).

    Returns:
        List of file paths where audio briefs were saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []

    for idx in batch_response.all_flagged:
        response = batch_response.results[idx]
        flagged_cats = [
            c.category for c in response.categories if c.flagged
        ]
        text_preview = texts[idx][:200] if idx < len(texts) else "unknown text"

        summary = (
            f"Case {idx + 1}. "
            f"Content preview: {text_preview}. "
            f"Flagged categories: {', '.join(flagged_cats)}. "
            f"Please review and make a determination."
        )

        filename = f"case_{idx + 1}.{response_format}"
        output_path = os.path.join(output_dir, filename)
        save_reviewer_brief_audio(
            summary,
            output_path,
            api_key=api_key,
            model=model,
            voice=voice,
            response_format=response_format,
        )
        saved_paths.append(output_path)

    return saved_paths
