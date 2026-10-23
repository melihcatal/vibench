"""
reviewer_brief_audio.py - Generate spoken briefs for moderation reviewers.

Uses the OpenAI Audio/Speech API (api.openai.com) with the tts-1-hd model
to generate audio briefs summarizing moderation cases for human reviewers.
"""

import os
import base64
from datetime import datetime

import openai


SPEECH_MODEL = "tts-1-hd"
DEFAULT_VOICE = "alloy"
DEFAULT_SPEED = 1.0
DEFAULT_RESPONSE_FORMAT = "mp3"

AVAILABLE_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def _get_openai_client():
    """Create an OpenAI client for audio/speech API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def generate_reviewer_brief_audio(
    case_summary: str,
    voice: str = DEFAULT_VOICE,
    speed: float = DEFAULT_SPEED,
    response_format: str = DEFAULT_RESPONSE_FORMAT,
) -> dict:
    """
    Generate an audio brief for a moderation case review.

    Args:
        case_summary: Text summary of the moderation case to read aloud.
        voice: Voice to use for speech synthesis (alloy, echo, fable, onyx, nova, shimmer).
        speed: Speech speed multiplier (0.25 to 4.0).
        response_format: Audio format ('mp3', 'opus', 'aac', 'flac').

    Returns:
        Dictionary with:
            - audio_base64: Base64-encoded audio data
            - format: audio format
            - voice: voice used
            - model: speech model used
            - provider: openai
    """
    client = _get_openai_client()

    # Format the brief text for natural speech
    brief_text = _format_brief_for_speech(case_summary)

    response = client.audio.speech.create(
        model=SPEECH_MODEL,
        voice=voice,
        input=brief_text,
        speed=speed,
        response_format=response_format,
    )

    audio_bytes = response.content
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio_base64": audio_base64,
        "audio_length_bytes": len(audio_bytes),
        "format": response_format,
        "voice": voice,
        "speed": speed,
        "model": SPEECH_MODEL,
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/audio/speech",
    }


def _format_brief_for_speech(case_summary: str) -> str:
    """Format case summary text for natural speech output."""
    # Add introductory phrase for context
    brief = f"Moderation case review. {case_summary}"

    # Clean up any problematic characters for TTS
    brief = brief.replace("*", "star").replace("#", "hash").replace("&", "and")

    return brief


def generate_batch_briefs(
    cases: list[dict],
    voice: str = DEFAULT_VOICE,
    speed: float = DEFAULT_SPEED,
) -> list[dict]:
    """
    Generate audio briefs for a batch of moderation cases.

    Args:
        cases: List of case dicts with 'case_id' and 'summary' keys.
        voice: Voice to use for all briefs.
        speed: Speech speed multiplier.

    Returns:
        List of audio generation results.
    """
    results = []

    for case in cases:
        case_summary = case.get("summary", "No summary available.")
        audio_result = generate_reviewer_brief_audio(
            case_summary=case_summary,
            voice=voice,
            speed=speed,
        )

        results.append({
            "case_id": case.get("case_id"),
            "audio_base64": audio_result["audio_base64"],
            "audio_length_bytes": audio_result["audio_length_bytes"],
            "voice": voice,
            "model": SPEECH_MODEL,
            "provider": "openai",
        })

    return results


def generate_escalation_brief(
    case_details: dict,
    reviewer_name: str = None,
    voice: str = DEFAULT_VOICE,
) -> dict:
    """
    Generate an audio brief for an escalated moderation case.

    Args:
        case_details: Dict with case information (case_id, decision, categories, etc.).
        reviewer_name: Name of the assigned reviewer (optional).
        voice: Voice to use for speech synthesis.

    Returns:
        Audio brief dict for the escalation.
    """
    case_id = case_details.get("case_id", "unknown")
    decision = case_details.get("decision", "under review")
    categories = case_details.get("flagged_categories", [])
    original_text = case_details.get("original_text", "")
    appeal_text = case_details.get("appeal_text", "")

    # Build escalation summary
    summary_parts = [f"Case {case_id} has been escalated for senior review."]
    summary_parts.append(f"Original decision: {decision}.")

    if categories:
        summary_parts.append(f"Flagged categories: {', '.join(categories)}.")

    if original_text:
        preview = original_text[:100] + ("..." if len(original_text) > 100 else "")
        summary_parts.append(f"Original content preview: {preview}")

    if appeal_text:
        summary_parts.append("User has submitted an appeal.")

    if reviewer_name:
        summary_parts.append(f"Assigned reviewer: {reviewer_name}.")

    summary_parts.append("Please review this case and provide your decision.")

    case_summary = " ".join(summary_parts)

    audio_result = generate_reviewer_brief_audio(
        case_summary=case_summary,
        voice=voice,
    )

    audio_result["case_id"] = case_id
    audio_result["escalation"] = True
    audio_result["reviewer"] = reviewer_name
    audio_result["generated_at"] = datetime.utcnow().isoformat()

    return audio_result


def get_voice_options() -> dict:
    """
    Return available voice options for speech generation.

    Returns:
        Dict of voice names and brief descriptions.
    """
    return {
        "voices": AVAILABLE_VOICES,
        "default_voice": DEFAULT_VOICE,
        "model": SPEECH_MODEL,
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/audio/speech",
    }


if __name__ == "__main__":
    sample_summary = "User content flagged for harassment. Categories: harassment, harassment/threatening. Appeal received stating content was taken out of context."
    result = generate_reviewer_brief_audio(sample_summary, voice="nova")
    print(f"Audio generated: {result['audio_length_bytes']} bytes")
    print(f"Format: {result['format']}, Voice: {result['voice']}, Model: {result['model']}")
