"""Local configuration and client helper utilities for Batch Speech-to-Text using AssemblyAI."""

import os
from typing import Optional

import assemblyai as aai


ASSEMBLYAI_API_HOST = "api.assemblyai.com"
DEFAULT_API_ENV_VAR = "ASSEMBLYAI_API_KEY"


def load_api_key(env_var: str = DEFAULT_API_ENV_VAR) -> str:
    """Load AssemblyAI API key from environment variable."""
    api_key = os.environ.get(env_var)
    if not api_key:
        raise ValueError(
            f"{env_var} environment variable must be set for AssemblyAI access"
        )
    return api_key


def create_client(api_key: Optional[str] = None) -> aai.AssemblyAI:
    """Create and configure an AssemblyAI client with the provider's settings."""
    if api_key is None:
        api_key = load_api_key()
    aai.settings.api_key = api_key
    return aai


def normalize_audio_url(audio_input: str) -> str:
    """Normalize audio input to a URL acceptable by AssemblyAI Transcripts API.

    AssemblyAI requires a publicly accessible URL or uploads the audio
    through their own upload mechanism.
    """
    if audio_input.startswith(("http://", "https://")):
        return audio_input
    if os.path.isfile(audio_input):
        return audio_input
    raise ValueError(
        f"Audio input must be a URL or a local file path, got: {audio_input}"
    )


def format_transcript_text(transcript: aai.Transcript) -> str:
    """Format an AssemblyAI transcript object into plain text."""
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    return transcript.text or ""


def extract_transcript_id(transcript: aai.Transcript) -> str:
    """Extract the unique identifier from a transcript submission."""
    return transcript.id
