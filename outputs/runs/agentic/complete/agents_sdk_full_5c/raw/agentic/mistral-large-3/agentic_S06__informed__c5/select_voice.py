from typing import List, Optional
import os
from elevenlabs.client import ElevenLabs
from speech_client import get_speech_client
from speech_models import VoiceInfo

client: Optional[ElevenLabs] = None

def _get_client() -> ElevenLabs:
    global client
    if client is None:
        client = get_speech_client()
    return client

def list_voices(locale: Optional[str] = None) -> List[VoiceInfo]:
    client = _get_client()
    voices = client.voices.get_all()
    
    voice_infos = []
    for voice in voices.voices:
        voice_infos.append(
            VoiceInfo(
                voice_id=voice.voice_id,
                name=voice.name,
                category=voice.category,
                languages=[lang.language_id for lang in voice.labels.get("accent", [])]
            )
        )
    
    if locale:
        voice_infos = [v for v in voice_infos if locale in v.languages]
    
    return voice_infos

def select_voice(locale: str) -> VoiceInfo:
    voices = list_voices(locale)
    if not voices:
        raise ValueError(f"No voices found for locale: {locale}")
    return voices[0]