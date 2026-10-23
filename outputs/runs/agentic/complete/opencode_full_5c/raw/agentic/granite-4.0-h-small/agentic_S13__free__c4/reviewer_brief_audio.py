# LATER-STEP: reviewer_brief_audio.py
"""Generate spoken briefs for moderation reviewers using a TTS service."""

import os
import tempfile
from typing import Optional

from safety_client import get_moderation_client

# --------------------------------------------------------------
# Placeholder for a text‑to‑speech (TTS) provider
# --------------------------------------------------------------
TTS_PROVIDER = os.getenv("TEXT_TTS_PROVIDER", "amazon")
TTS_API_KEY = os.getenv("TEXT_TTS_API_KEY")


def generate_brief_audio(reason: str, output_path: Optional[str] = None) -> str:
    """Create an audio file with a spoken moderation brief.

    Args:
        reason: Human‑readable explanation of the moderation decision.
        output_path: Destination file for the audio (default = temporary file).

    Returns:
        Path to the generated audio file.
    """
    if not TTS_API_KEY:
        raise RuntimeError("TEXT_TTS_API_KEY environment variable must be set")

    if TTS_PROVIDER == "amazon":
        # AWS Polly example (stub)
        try:
            import boto3

            client = boto3.client(
                "polly", region_name="us-east-1", aws_access_key_id=TTS_API_KEY
            )
            response = client.synthesize_speech(
                Text=reason,
                OutputFormat="mp3",
                VoiceId="Joanna",
            )
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(response["AudioStream"].read())
                return output_path
            else:
                # write to a temporary file and return its path
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp.write(response["AudioStream"].read())
                    return tmp.name
        except Exception as e:
            raise RuntimeError("AWS Polly failed") from e
    elif TTS_PROVIDER == "google":
        # Google Cloud Text‑to‑Speech example (stub)
        raise NotImplementedError("Google TTS provider not implemented")
    else:
        raise RuntimeError(f"Unsupported TTS provider: {TTS_PROVIDER}")
