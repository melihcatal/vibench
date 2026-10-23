import base64
import io
import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"


def _extract_text(platform_output: Any) -> str:
    if platform_output is None:
        return ""
    if isinstance(platform_output, str):
        return platform_output
    if isinstance(platform_output, bytes):
        return platform_output.decode("utf-8", errors="ignore")
    if isinstance(platform_output, dict):
        for key in ("text", "output_text", "content", "message", "briefing"):
            value = platform_output.get(key)
            if isinstance(value, str) and value.strip():
                return value
        for key in ("choices", "outputs", "data", "items"):
            value = platform_output.get(key)
            if isinstance(value, list) and value:
                for item in value:
                    extracted = _extract_text(item)
                    if extracted:
                        return extracted
        return " ".join(str(v) for v in platform_output.values() if isinstance(v, str))
    if isinstance(platform_output, (list, tuple)):
        parts = []
        for item in platform_output:
            extracted = _extract_text(item)
            if extracted:
                parts.append(extracted)
        return " ".join(parts)
    return str(platform_output)


def _build_briefing_prompt(text: str, locale: str) -> str:
    return (
        f"Create a concise spoken briefing in {locale}. "
        f"Keep it natural and easy to read aloud.\n\n{text.strip()}"
    )


def generate_spoken_briefing(platform_output: Any, locale: str = "en-US", voice: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    source_text = _extract_text(platform_output).strip()
    prompt = _build_briefing_prompt(source_text, locale)
    response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=voice or DEFAULT_VOICE,
        input=prompt,
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "provider": "openai",
        "model": DEFAULT_TTS_MODEL,
        "voice": voice or DEFAULT_VOICE,
        "locale": locale,
        "briefing_text": source_text,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
        "content_type": "audio/mpeg",
    }
