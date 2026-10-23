import os
from typing import Dict, Any
from openai import OpenAI
import base64


def reviewer_brief_audio(moderation_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers using OpenAI's TTS API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    total_items = moderation_summary.get("total_items", 0)
    flagged_items = moderation_summary.get("flagged_items", 0)
    moderation_rate = moderation_summary.get("moderation_rate", 0)

    brief_text = f"""
    Moderation Review Brief.
    Total items reviewed: {total_items}.
    Flagged items: {flagged_items}.
    Moderation rate: {moderation_rate:.1%}.
    """

    if "most_common_categories" in moderation_summary:
        categories = moderation_summary["most_common_categories"]
        if categories:
            brief_text += f" Most common violation categories: {', '.join(categories)}."

    if "patterns" in moderation_summary:
        patterns = moderation_summary["patterns"]
        if patterns:
            brief_text += f" Notable patterns: {patterns}."

    try:
        response = client.audio.speech.create(
            model="tts-1", voice="alloy", input=brief_text
        )

        audio_content = response.content
        audio_base64 = base64.b64encode(audio_content).decode("utf-8")

        return {
            "brief_text": brief_text,
            "audio_base64": audio_base64,
            "audio_format": "mp3",
            "voice_model": "tts-1",
            "voice": "alloy",
            "total_items": total_items,
            "flagged_items": flagged_items,
            "moderation_rate": moderation_rate,
        }

    except Exception as e:
        return {
            "brief_text": brief_text,
            "audio_base64": None,
            "error": str(e),
            "total_items": total_items,
            "flagged_items": flagged_items,
            "moderation_rate": moderation_rate,
        }
