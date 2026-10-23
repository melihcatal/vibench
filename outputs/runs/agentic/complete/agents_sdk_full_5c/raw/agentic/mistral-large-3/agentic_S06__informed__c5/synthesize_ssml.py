from typing import Optional
import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse

client: Optional[ElevenLabs] = None

def _get_client() -> ElevenLabs:
    global client
    if client is None:
        client = get_speech_client()
    return client

def synthesize_ssml(request: SynthesisRequest) -> SynthesisResponse:
    client = _get_client()
    voice_id = request.voice_id or "pNInz6obpgDQGcFmaJgB"  # ElevenLabs premade voice
    
    audio = client.generate(
        text=request.text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    )
    
    return SynthesisResponse(audio_bytes=audio, mime_type="audio/mpeg")