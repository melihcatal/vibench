"""
Generate spoken briefs for moderation reviewers using Amazon Polly.

Provider: Amazon Polly
SDK: boto3
"""

import base64
import os
from typing import Optional

import boto3

from safety_models import BatchModerationResponse, ModerationResponse


def _build_reviewer_brief_text(moderation_results: list) -> str:
    """Construct a spoken-brief script from moderation results."""
    total = len(moderation_results)
    flagged = [m for m in moderation_results if not m.is_safe]
    flagged_count = len(flagged)

    lines = []
    lines.append(f"Moderation review brief. {total} messages were analyzed.")
    if flagged_count == 0:
        lines.append("All messages passed safety checks. No action required.")
    else:
        lines.append(f"{flagged_count} messages were flagged for review.")
        for i, mod in enumerate(flagged, 1):
            cats = ", ".join(
                f"{c.category} at severity {c.severity}"
                for c in mod.categories
                if c.is_flagged
            )
            lines.append(
                f"Flagged message {i}: {cats}. "
                f"Original text: {mod.text[:100]}..."
            )
    lines.append("End of brief.")
    return " ".join(lines)


def generate_reviewer_audio(
    moderation_results: list,
    voice_id: str = "Joanna",
    region: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    output_format: str = "mp3",
) -> bytes:
    """
    Generate an audio brief for moderation reviewers using Amazon Polly.

    Provider: Amazon Polly
    Voice: configurable via voice_id (default: Joanna)

    Args:
        moderation_results: List of ModerationResponse objects.
        voice_id: Amazon Polly voice ID (e.g., Joanna, Matthew, Ivy).
        region: AWS region for Polly service.
        aws_access_key_id: Optional AWS access key.
        aws_secret_access_key: Optional AWS secret key.
        output_format: Audio format (mp3, ogg_vorbis, pcm).

    Returns:
        Audio bytes in the requested format.
    """
    kwargs = {}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if region:
        kwargs["region_name"] = region

    polly = boto3.client("polly", **kwargs)

    brief_text = _build_reviewer_brief_text(moderation_results)

    response = polly.synthesize_speech(
        Text=brief_text,
        OutputFormat=output_format,
        VoiceId=voice_id,
    )

    audio_stream = response.get("AudioStream")
    if audio_stream is None:
        raise RuntimeError("Amazon Polly returned no audio stream.")

    return audio_stream.read()


def generate_reviewer_audio_from_batch(
    batch_response: BatchModerationResponse,
    voice_id: str = "Joanna",
    region: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    output_format: str = "mp3",
) -> bytes:
    """Convenience wrapper accepting a BatchModerationResponse."""
    results = [r.moderation for r in batch_response.results]
    return generate_reviewer_audio(
        results,
        voice_id=voice_id,
        region=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        output_format=output_format,
    )


def save_reviewer_audio(
    moderation_results: list,
    filepath: str,
    voice_id: str = "Joanna",
    region: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    output_format: str = "mp3",
) -> str:
    """Generate and save reviewer audio to a file. Returns the filepath."""
    audio_bytes = generate_reviewer_audio(
        moderation_results,
        voice_id=voice_id,
        region=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        output_format=output_format,
    )
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    return filepath


if __name__ == "__main__":
    sample_moderations = []
    audio = generate_reviewer_audio(sample_moderations, voice_id="Joanna")
    print(f"Generated {len(audio)} bytes of audio.")
