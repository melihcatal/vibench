"""
Generate spoken briefs for moderation reviewers using text-to-speech.
Provider: ElevenLabs Text to Speech via elevenlabs SDK.
Auth: ELEVENLABS_API_KEY
"""

import os
import json
from typing import Optional, List, Dict

from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")


def _build_reviewer_brief(moderation_case: Dict) -> str:
    """Build a spoken brief script from a moderation case."""
    case_id = moderation_case.get("case_id", "Unknown")
    content_preview = moderation_case.get("content_preview", "")
    decision = moderation_case.get("decision", "Pending")
    reasons = moderation_case.get("reasons", [])
    categories = moderation_case.get("categories", [])

    brief = f"Review case {case_id}. "
    brief += f"Content preview: {content_preview}. "
    brief += f"Decision: {decision}. "

    if categories:
        brief += f"Flagged categories: {', '.join(categories)}. "

    if reasons:
        brief += "Reasons: " + ". ".join(reasons) + ". "

    brief += "Please review this case and confirm or appeal the decision."
    return brief


def reviewer_brief_audio(
    moderation_case: Dict,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model_id: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> bytes:
    """
    Generate a spoken audio brief for a moderation reviewer using ElevenLabs TTS.

    Args:
        moderation_case: Dict with case_id, content_preview, decision, reasons, categories.
        voice_id: ElevenLabs voice ID (default: Bella voice).
        model_id: ElevenLabs model identifier (default: eleven_multilingual_v2).
        api_key: Optional ElevenLabs API key override.

    Returns:
        Audio bytes in MP3 format.
    """
    key = api_key or ELEVENLABS_API_KEY
    if not key:
        raise ValueError("ELEVENLABS_API_KEY is required for ElevenLabs Text to Speech.")

    client = ElevenLabs(api_key=key)

    brief_text = _build_reviewer_brief(moderation_case)

    audio = client.generate(
        text=brief_text,
        voice=voice_id,
        model=model_id,
    )

    audio_bytes = b"".join(audio)
    return audio_bytes


def reviewer_brief_audio_json(
    moderation_case: Dict,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model_id: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Dict:
    """
    Generate spoken brief audio and return metadata with optional file save.

    Args:
        moderation_case: Dict with moderation case details.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model identifier.
        api_key: Optional ElevenLabs API key override.
        output_path: Optional file path to save the audio.

    Returns:
        Dictionary with brief text, audio size, model info, and provider.
    """
    audio_bytes = reviewer_brief_audio(
        moderation_case=moderation_case,
        voice_id=voice_id,
        model_id=model_id,
        api_key=api_key,
    )

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    brief_text = _build_reviewer_brief(moderation_case)

    return {
        "brief_text": brief_text,
        "audio_size_bytes": len(audio_bytes),
        "voice_id": voice_id,
        "model": model_id,
        "format": "mp3",
        "provider": "ElevenLabs Text to Speech",
        "saved_to": output_path,
    }


def reviewer_brief_batch_audio(
    moderation_cases: List[Dict],
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model_id: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict:
    """
    Generate spoken briefs for multiple moderation cases.

    Args:
        moderation_cases: List of moderation case dicts.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model identifier.
        api_key: Optional ElevenLabs API key override.
        output_dir: Optional directory to save audio files.

    Returns:
        Dictionary with batch generation metadata.
    """
    key = api_key or ELEVENLABS_API_KEY
    if not key:
        raise ValueError("ELEVENLABS_API_KEY is required for ElevenLabs Text to Speech.")

    client = ElevenLabs(api_key=key)
    results = []

    for case in moderation_cases:
        case_id = case.get("case_id", "unknown")
        brief_text = _build_reviewer_brief(case)

        audio = client.generate(
            text=brief_text,
            voice=voice_id,
            model=model_id,
        )
        audio_bytes = b"".join(audio)

        output_path = None
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"brief_{case_id}.mp3")
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        results.append({
            "case_id": case_id,
            "brief_text": brief_text,
            "audio_size_bytes": len(audio_bytes),
            "saved_to": output_path,
        })

    return {
        "results": results,
        "total_count": len(moderation_cases),
        "voice_id": voice_id,
        "model": model_id,
        "provider": "ElevenLabs Text to Speech",
    }


if __name__ == "__main__":
    sample_case = {
        "case_id": "CASE-2024-001",
        "content_preview": "User posted content flagged for policy violation.",
        "decision": "Suspended",
        "reasons": ["Hate speech targeting a protected group"],
        "categories": ["Hate"],
    }
    result = reviewer_brief_audio_json(sample_case)
    print(json.dumps(result, indent=2))
