"""
[LATER-STEP] reviewer_brief_audio.py - Generate spoken briefs for moderation reviewers.

Uses the OpenAI Text-to-Speech API (model: tts-1) to generate audio briefs
summarizing moderation cases for reviewers who prefer audio-based workflows.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


_TTS_MODEL = "tts-1"
_TTS_HD_MODEL = "tts-1-hd"
_DEFAULT_VOICE = "alloy"

_VOICE_OPTIONS = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def _build_brief_text(
    case_id: str,
    moderation_reason: str,
    appeal_text: Optional[str] = None,
    severity: Optional[str] = None,
    recommended_action: Optional[str] = None,
) -> str:
    """Construct a natural-language brief from moderation case details."""
    parts = [
        f"Moderation case {case_id}.",
    ]
    if severity:
        parts.append(f"Severity level: {severity}.")
    parts.append(f"Moderation reason: {moderation_reason}.")
    if appeal_text:
        parts.append(f"User appeal: {appeal_text}.")
    if recommended_action:
        parts.append(f"Recommended action: {recommended_action}.")
    return " ".join(parts)


def generate_reviewer_brief_audio(
    case_id: str,
    moderation_reason: str,
    output_path: str,
    api_key: Optional[str] = None,
    appeal_text: Optional[str] = None,
    severity: Optional[str] = None,
    recommended_action: Optional[str] = None,
    voice: str = _DEFAULT_VOICE,
    model: str = _TTS_MODEL,
    speed: float = 1.0,
) -> Path:
    """
    Generate an audio brief for a moderation review case using OpenAI TTS.

    Parameters
    ----------
    case_id : str
        Unique identifier for the moderation case.
    moderation_reason : str
        The reason the content was flagged.
    output_path : str
        File path where the MP3 audio will be saved.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var.
    appeal_text : str, optional
        The user's appeal text, if available.
    severity : str, optional
        The severity classification (e.g., "high", "critical").
    recommended_action : str, optional
        Recommended reviewer action.
    voice : str
        TTS voice to use (default: alloy). Options: alloy, echo, fable,
        onyx, nova, shimmer.
    model : str
        OpenAI TTS model (default: tts-1). Use tts-1-hd for higher quality.
    speed : float
        Speech speed multiplier (0.25 to 4.0, default: 1.0).

    Returns
    -------
    Path
        The path to the generated MP3 file.
    """
    brief_text = _build_brief_text(
        case_id,
        moderation_reason,
        appeal_text=appeal_text,
        severity=severity,
        recommended_action=recommended_action,
    )

    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    speed_clamped = max(0.25, min(4.0, speed))

    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=brief_text,
            speed=speed_clamped,
            response_format="mp3",
        )
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        response.stream_to_file(str(output))
        return output
    finally:
        if hasattr(client, "close"):
            client.close()


def generate_brief_audio_from_summary(
    summary: dict,
    output_path: str,
    api_key: Optional[str] = None,
    voice: str = _DEFAULT_VOICE,
    model: str = _TTS_MODEL,
) -> Path:
    """
    Generate an audio brief from a moderation summary dict (as produced by
    moderation_summary.py).

    Parameters
    ----------
    summary : dict
        The structured moderation summary with keys like overall_verdict,
        summary, key_concerns, recommended_action.
    output_path : str
        File path for the output MP3.
    api_key : str, optional
        OpenAI API key.
    voice : str
        TTS voice to use.
    model : str
        OpenAI TTS model.

    Returns
    -------
    Path
        The path to the generated MP3 file.
    """
    brief_text = _build_brief_text(
        case_id=summary.get("case_id", "unknown"),
        moderation_reason=summary.get("summary", ""),
        severity=str(summary.get("risk_level", "N/A")),
        recommended_action=summary.get("recommended_action", ""),
    )
    return generate_reviewer_brief_audio(
        case_id=summary.get("case_id", "unknown"),
        moderation_reason=summary.get("summary", ""),
        output_path=output_path,
        api_key=api_key,
        severity=str(summary.get("risk_level", "N/A")),
        recommended_action=summary.get("recommended_action", ""),
        voice=voice,
        model=model,
    )


def main() -> None:
    import sys
    if len(sys.argv) < 4:
        print("Usage: python reviewer_brief_audio.py <case_id> <moderation_reason> <output.mp3>")
        sys.exit(1)
    case_id = sys.argv[1]
    reason = sys.argv[2]
    output = sys.argv[3]
    path = generate_reviewer_brief_audio(case_id, reason, output)
    print(f"Audio brief saved to: {path}")


if __name__ == "__main__":
    main()
