from __future__ import annotations

from typing import List, Optional

from speech_client import build_client, get_text_to_speech_provider
from speech_models import VoiceProfile


def select_voice(locale: str, preference: Optional[str] = None) -> List[VoiceProfile]:
    provider = get_text_to_speech_provider()
    client = build_client()
    profiles: List[VoiceProfile] = []
    if provider == "google":
        voices = client.list_voices(language_code=locale).voices
        for voice in voices:
            profiles.append(VoiceProfile(name=voice.name, language_codes=list(voice.language_codes), gender=getattr(voice.ssml_gender, "name", str(voice.ssml_gender)), provider="google"))
    elif provider == "azure":
        voices = client.get_voices()
        for voice in voices.voices:
            if locale.lower() in (voice.Locale or "").lower():
                profiles.append(VoiceProfile(name=voice.ShortName, language_codes=[voice.Locale], gender=voice.Gender, provider="azure", style=getattr(voice, "StyleList", None)))
    elif provider == "aws":
        response = client.describe_voices(LanguageCode=locale)
        for voice in response.get("Voices", []):
            profiles.append(VoiceProfile(name=voice["Id"], language_codes=[voice.get("LanguageCode", locale)], gender=voice.get("Gender", "Neutral"), provider="aws"))
    elif provider == "openai":
        profiles.append(VoiceProfile(name=preference or "alloy", language_codes=[locale], gender="neutral", provider="openai", model="gpt-4o-mini-tts"))
    elif provider == "elevenlabs":
        import requests

        api_key = client
        response = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": api_key}, timeout=30)
        response.raise_for_status()
        for voice in response.json().get("voices", []):
            labels = voice.get("labels", {})
            if locale.lower() in str(labels.get("language", locale)).lower():
                profiles.append(VoiceProfile(name=voice.get("name", ""), language_codes=[labels.get("language", locale)], gender=labels.get("gender", "neutral"), provider="elevenlabs", voice_id=voice.get("voice_id")))
    if preference:
        profiles.sort(key=lambda v: 0 if preference.lower() in v.name.lower() else 1)
    return profiles
