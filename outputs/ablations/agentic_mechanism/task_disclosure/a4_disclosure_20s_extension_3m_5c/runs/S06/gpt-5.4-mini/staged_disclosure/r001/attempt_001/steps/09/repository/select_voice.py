import os
import sys
from typing import Any, Dict, List, Optional

from elevenlabs.client import ElevenLabs


def _client() -> ElevenLabs:
    return ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])


def _normalize_locale(locale: str) -> str:
    return locale.strip().lower().replace("_", "-")


def _voice_matches_locale(voice: Dict[str, Any], locale: str) -> bool:
    target = _normalize_locale(locale)
    labels: List[str] = []

    for key in ("labels", "metadata"):
        value = voice.get(key)
        if isinstance(value, dict):
            labels.extend(str(v) for v in value.values() if v is not None)

    for key in ("name", "voice_id", "category"):
        value = voice.get(key)
        if value is not None:
            labels.append(str(value))

    return any(target in _normalize_locale(label) for label in labels)


def select_voice(locale: str, preferred_voice_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    client = _client()
    voices = client.voices.get_all().voices

    if preferred_voice_id:
        for voice in voices:
            if getattr(voice, "voice_id", None) == preferred_voice_id:
                return voice.__dict__ if hasattr(voice, "__dict__") else voice

    for voice in voices:
        payload = voice.__dict__ if hasattr(voice, "__dict__") else voice
        if isinstance(payload, dict) and _voice_matches_locale(payload, locale):
            return payload

    return None


def _main() -> None:
    locale = os.environ.get("TARGET_LOCALE", "en-US")
    preferred_voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
    voice = select_voice(locale, preferred_voice_id=preferred_voice_id)
    if voice is None:
        sys.exit(1)
    voice_id = voice.get("voice_id") if isinstance(voice, dict) else getattr(voice, "voice_id", None)
    name = voice.get("name") if isinstance(voice, dict) else getattr(voice, "name", None)
    print(f"{voice_id}\t{name}")


if __name__ == "__main__":
    _main()
