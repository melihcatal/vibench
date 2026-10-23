import base64
import io
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class PlatformBriefAudioResult:
    text: str
    audio_bytes: bytes
    metadata: Dict[str, Any]


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_spoken_briefing(platform_output: str, voice: str = "alloy") -> PlatformBriefAudioResult:
    client = _client()
    briefing_prompt = (
        "Create a concise spoken briefing from the following platform output. "
        "Preserve key findings, names, and metrics, and make it sound natural when read aloud.\n\n"
        f"Platform output:\n{platform_output}"
    )
    text_response = client.responses.create(
        model="gpt-5.4-mini",
        input=briefing_prompt,
    )
    briefing_text = text_response.output_text
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=briefing_text,
        format="mp3",
    )
    audio_content = getattr(speech, "content", None)
    if audio_content is None:
        buffer = io.BytesIO()
        speech.stream_to_file(buffer)
        audio_bytes = buffer.getvalue()
    else:
        audio_bytes = audio_content if isinstance(audio_content, bytes) else base64.b64decode(audio_content)
    return PlatformBriefAudioResult(
        text=briefing_text,
        audio_bytes=audio_bytes,
        metadata={"provider": "openai", "text_model": "gpt-5.4-mini", "audio_model": "gpt-4o-mini-tts", "voice": voice},
    )
