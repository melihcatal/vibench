import os
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient

DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def _build_reviewer_brief_text(summary: dict) -> str:
    lines = []
    exec_summary = summary.get("executive_summary", "No summary available.")
    lines.append(f"Executive Summary: {exec_summary}")
    risk = summary.get("risk_assessment", "No risk assessment provided.")
    lines.append(f"Risk Assessment: {risk}")
    actions = summary.get("recommended_actions", [])
    if isinstance(actions, list):
        lines.append("Recommended Actions:")
        for action in actions:
            lines.append(f"  - {action}")
    elif isinstance(actions, str):
        lines.append(f"Recommended Actions: {actions}")
    breakdown = summary.get("category_breakdown", {})
    if breakdown:
        lines.append("Category Breakdown:")
        for cat, info in breakdown.items():
            lines.append(f"  - {cat}: {info}")
    lines.append(f"Total messages reviewed: {summary.get('total_messages', 0)}")
    lines.append(f"Flagged: {summary.get('flagged_count', 0)}")
    lines.append(f"Safe: {summary.get('safe_count', 0)}")
    return "\n".join(lines)


def reviewer_brief_audio(
    moderation_summary: dict,
    api_key: str | None = None,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
) -> bytes:
    client = ElevenLabs(api_key=api_key)
    brief_text = _build_reviewer_brief_text(moderation_summary)
    audio = client.generate(
        text=brief_text,
        voice=voice_id,
        model=model_id,
    )
    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk
    return audio_bytes


def generate_brief_audio_from_text(
    text: str,
    api_key: str | None = None,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
) -> bytes:
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
    )
    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk
    return audio_bytes


def save_reviewer_brief_audio(
    moderation_summary: dict,
    output_path: str,
    api_key: str | None = None,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
) -> str:
    audio_bytes = reviewer_brief_audio(
        moderation_summary=moderation_summary,
        api_key=api_key,
        voice_id=voice_id,
        model_id=model_id,
    )
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path
