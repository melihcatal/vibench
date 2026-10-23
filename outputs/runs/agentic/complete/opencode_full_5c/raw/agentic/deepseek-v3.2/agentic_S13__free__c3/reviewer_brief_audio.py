import os
from openai import OpenAI
from typing import Dict, Any
import base64


def reviewer_brief_audio(moderation_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers using OpenAI's TTS API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    total_messages = moderation_summary.get("actual_total", 0)
    flagged_count = moderation_summary.get("actual_flagged", 0)
    category_counts = moderation_summary.get("category_counts", {})

    brief_text = f"""
    Moderation Review Brief.
    Total messages analyzed: {total_messages}.
    Flagged messages: {flagged_count}.
    """

    if category_counts:
        brief_text += "Violation categories: "
        for category, count in category_counts.items():
            brief_text += f"{category}: {count}. "

    safety_assessment = moderation_summary.get(
        "safety_assessment", "No assessment provided"
    )
    brief_text += f"Overall safety assessment: {safety_assessment}."

    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text, response_format="mp3"
    )

    audio_content = response.content

    return {
        "audio_content": base64.b64encode(audio_content).decode("utf-8"),
        "audio_format": "mp3",
        "brief_text": brief_text,
        "total_messages": total_messages,
        "flagged_count": flagged_count,
        "category_counts": category_counts,
        "tts_model": "tts-1",
        "voice": "alloy",
        "provider": "OpenAI",
    }


def save_audio_brief(
    moderation_summary: Dict[str, Any], output_path: str
) -> Dict[str, Any]:
    """
    Generate and save audio brief to file.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    total_messages = moderation_summary.get("actual_total", 0)
    flagged_count = moderation_summary.get("actual_flagged", 0)
    category_counts = moderation_summary.get("category_counts", {})

    brief_text = f"""
    Moderation Review Brief.
    Total messages analyzed: {total_messages}.
    Flagged messages: {flagged_count}.
    """

    if category_counts:
        brief_text += "Violation categories: "
        for category, count in category_counts.items():
            brief_text += f"{category}: {count}. "

    safety_assessment = moderation_summary.get(
        "safety_assessment", "No assessment provided"
    )
    brief_text += f"Overall safety assessment: {safety_assessment}."

    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text, response_format="mp3"
    )

    response.stream_to_file(output_path)

    return {
        "output_path": output_path,
        "brief_text": brief_text,
        "total_messages": total_messages,
        "flagged_count": flagged_count,
        "category_counts": category_counts,
        "tts_model": "tts-1",
        "voice": "alloy",
        "provider": "OpenAI",
        "file_size": os.path.getsize(output_path) if os.path.exists(output_path) else 0,
    }
