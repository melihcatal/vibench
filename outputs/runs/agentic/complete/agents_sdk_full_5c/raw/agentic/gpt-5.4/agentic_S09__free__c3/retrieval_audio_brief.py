from __future__ import annotations

from collections.abc import Sequence

from elevenlabs.client import ElevenLabs


VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


def retrieval_audio_brief(results: Sequence[dict], voice_id: str = VOICE_ID) -> bytes:
    client = ElevenLabs()
    brief_lines = []
    for idx, item in enumerate(results[:5], start=1):
        title = item.get("title") or item.get("document") or f"Result {idx}"
        score = item.get("score")
        snippet = item.get("snippet") or item.get("document") or ""
        brief_lines.append(f"{idx}. {title}. Score {score}. {snippet}")
    script = "Summarize the top retrieval results for the listener: " + " ".join(brief_lines)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=script,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
