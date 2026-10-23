from typing import Dict, Any
from gtts import gTTS
import os


def reviewer_brief_audio(
    summary: Dict[str, Any], output_file: str = "review_brief.mp3"
) -> Dict[str, Any]:
    """
    Generates spoken briefs for moderation reviewers using Google Text-to-Speech (gTTS).
    """
    brief_text = (
        f"Moderation summary: {summary.get('total_messages', 0)} messages processed. "
        f"{summary.get('allowed', 0)} allowed, {summary.get('blocked', 0)} blocked. "
        f"Violations: {', '.join(f'{k}: {v}' for k, v in summary.get('violation_categories', {}).items())}"
    )

    tts = gTTS(text=brief_text, lang="en")
    tts.save(output_file)

    return {
        "brief_text": brief_text,
        "output_file": output_file,
        "provider": "gTTS (Google Text-to-Speech)",
    }
