from __future__ import annotations

import base64
import time
from typing import Any

from safety_client import call_elevenlabs_tts, load_elevenlabs_api_key
from safety_models import AudioResult, ModerationResult

ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_MODEL = "eleven_monolingual_v1"
ELEVENLABS_FORMAT = "mp3_44100_128"


async def generate_reviewer_brief_audio(
    moderation_results: list[ModerationResult],
    voice_id: str = ELEVENLABS_VOICE_ID,
    model: str = ELEVENLABS_MODEL,
    output_format: str = ELEVENLABS_FORMAT,
    api_key: str | None = None,
) -> AudioResult:
    if api_key is None:
        api_key = load_elevenlabs_api_key()

    brief_text = _build_reviewer_brief_text(moderation_results)

    audio_bytes = await call_elevenlabs_tts(
        text=brief_text,
        voice_id=voice_id,
        api_key=api_key,
        model=model,
        output_format=output_format,
    )

    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_url = f"data:audio/mpeg;base64,{audio_b64}"

    duration_seconds = _estimate_duration(brief_text)

    return AudioResult(
        text=brief_text,
        audio_url=audio_url,
        audio_format=output_format,
        duration_seconds=duration_seconds,
        model=model,
    )


def _build_reviewer_brief_text(results: list[ModerationResult]) -> str:
    total = len(results)
    flagged = sum(1 for r in results if r.flagged)
    blocked = sum(1 for r in results if r.action.value == "block")

    lines = [
        f"Moderation review briefing. {total} items processed, {flagged} flagged, {blocked} blocked.",
        "Key items requiring your attention:",
    ]

    sorted_results = sorted(results, key=lambda x: x.highest_score, reverse=True)
    for i, r in enumerate(sorted_results[:10]):
        if r.flagged:
            flagged_cats = [c.category for c in r.categories if c.flagged]
            lines.append(
                f"Item {i + 1}: Score {r.highest_score:.2f}. "
                f"Categories: {', '.join(flagged_cats)}. "
                f"Action: {r.action.value}. "
                f"Details: {r.rationale}"
            )

    if not any(r.flagged for r in results):
        lines.append("No flagged items. All content passed moderation checks.")

    lines.append("End of briefing.")
    return "\n".join(lines)


def _estimate_duration(text: str, words_per_minute: int = 150) -> float:
    word_count = len(text.split())
    return round((word_count / words_per_minute) * 60, 2)
