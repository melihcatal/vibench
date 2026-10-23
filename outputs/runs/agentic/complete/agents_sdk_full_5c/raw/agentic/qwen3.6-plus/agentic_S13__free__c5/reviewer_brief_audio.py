"""
[LATER-STEP] reviewer_brief_audio.py
Generate spoken briefs for moderation reviewers using ElevenLabs TTS.
Provider: ElevenLabs — API hostname: api.elevenlabs.io
"""

from typing import Optional, Dict, Any
import requests
import os
import base64

from safety_client import get_elevenlabs_api_key, load_safety_config
from safety_models import ReviewerAudioBrief

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs "Rachel" voice
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def build_brief_script(case_data: Dict[str, Any]) -> str:
    """
    Build a spoken briefing script from moderation case data for the reviewer.
    """
    text = case_data.get("summary", "Moderation case review.")
    flagged_categories = case_data.get("flagged_categories", [])
    risk_score = case_data.get("risk_score", 0.0)
    recommendation = case_data.get("recommendation", "Please review.")

    script_parts = [text]
    if flagged_categories:
        cats = ", ".join(flagged_categories)
        script_parts.append(f"Flagged categories: {cats}.")
    script_parts.append(f"Risk score: {risk_score:.2f}.")
    script_parts.append(recommendation)

    return " ".join(script_parts)


def generate_reviewer_brief_audio(
    case_data: Dict[str, Any],
    voice_id: str = DEFAULT_VOICE_ID,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    return_base64: bool = True,
    config: Optional[Dict[str, Any]] = None,
) -> ReviewerAudioBrief:
    """
    Generate a spoken moderation brief for a human reviewer using the
    ElevenLabs text-to-speech API (api.elevenlabs.io).

    The case_data dict should include:
      - summary: text summary of the case
      - flagged_categories: list of flagged category names
      - risk_score: float risk score
      - recommendation: recommendation text
    """
    if config is None:
        config = load_safety_config()

    api_key = get_elevenlabs_api_key(config)
    script = build_brief_script(case_data)

    tts_url = ELEVENLABS_TTS_URL.format(voice_id=voice_id)

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "output_format": output_format,
    }

    response = requests.post(
        tts_url,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    audio_base64 = None
    audio_url = None

    if return_base64:
        audio_bytes = response.content
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    else:
        audio_url = tts_url

    content_length = response.headers.get("content-length")
    duration_seconds = None
    if content_length:
        duration_seconds = int(content_length) / (44100 * 2)

    return ReviewerAudioBrief(
        case_summary=script,
        audio_base64=audio_base64,
        audio_url=audio_url,
        voice_id=voice_id,
        duration_seconds=duration_seconds,
        format="mp3",
    )


def generate_reviewer_brief_audio_dict(
    case_data: Dict[str, Any],
    voice_id: str = DEFAULT_VOICE_ID,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate a reviewer audio brief and return as a dict."""
    result = generate_reviewer_brief_audio(
        case_data, voice_id=voice_id, output_format=output_format, config=config
    )
    return result.to_dict()


if __name__ == "__main__":
    case = {
        "summary": "User submitted content with violent imagery.",
        "flagged_categories": ["violence", "violence_graphic"],
        "risk_score": 0.87,
        "recommendation": "Please review and make a final determination.",
    }
    result = generate_reviewer_brief_audio_dict(case)
    print(f"Generated brief for voice {result['voice_id']}")
