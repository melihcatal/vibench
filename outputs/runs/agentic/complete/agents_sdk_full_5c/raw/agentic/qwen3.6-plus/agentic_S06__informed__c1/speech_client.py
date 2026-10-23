"""
Local helper: speech_client.py
Provide local configuration and client helper utilities for Text-to-Speech.
Uses ElevenLabs as the concrete TTS provider.
"""
import os
from typing import Optional, Dict, Any
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from speech_models import (
    TTSRequest,
    SSMLRequest,
    TTSResponse,
    VoiceInfo,
    VoiceListResponse,
    VoiceGender,
    AudioFormat,
    normalize_audio_format,
)

DEFAULT_ELEVENLABS_MODEL = "eleven_multilingual_v2"
DEFAULT_STABILITY = 0.5
DEFAULT_SIMILARITY_BOOST = 0.75
DEFAULT_VOICE = "Rachel"

ELEVENLABS_AUDIO_FORMAT_MAP: Dict[AudioFormat, str] = {
    AudioFormat.MP3: "mp3_44100_128",
    AudioFormat.WAV: "pcm_44100",
    AudioFormat.OGG: "ogg_44100",
    AudioFormat.FLAC: "flac_44100",
    AudioFormat.PCM: "pcm_44100",
}


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    """Create and return an ElevenLabs client instance."""
    key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "ELEVENLABS_API_KEY environment variable is not set and no api_key provided."
        )
    return ElevenLabs(api_key=key)


def build_voice_settings(
    stability: float = DEFAULT_STABILITY,
    similarity_boost: float = DEFAULT_SIMILARITY_BOOST,
) -> VoiceSettings:
    """Build an ElevenLabs VoiceSettings object from normalized parameters."""
    return VoiceSettings(
        stability=stability,
        similarity_boost=similarity_boost,
    )


def resolve_audio_format_key(audio_format: AudioFormat) -> str:
    """Map local AudioFormat enum to ElevenLabs output format string."""
    return ELEVENLABS_AUDIO_FORMAT_MAP.get(audio_format, "mp3_44100_128")


def normalize_elevenlabs_response(
    audio_bytes: bytes,
    voice_id: str = "",
    model_id: str = DEFAULT_ELEVENLABS_MODEL,
    audio_format: AudioFormat = AudioFormat.MP3,
) -> TTSResponse:
    """Convert raw ElevenLabs audio bytes into a normalized TTSResponse."""
    content_type_map = {
        AudioFormat.MP3: "audio/mpeg",
        AudioFormat.WAV: "audio/wav",
        AudioFormat.OGG: "audio/ogg",
        AudioFormat.FLAC: "audio/flac",
        AudioFormat.PCM: "audio/pcm",
    }
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type_map.get(audio_format, "audio/mpeg"),
        voice_id=voice_id,
        model_id=model_id,
        metadata={"provider": "elevenlabs", "format": audio_format.value},
    )


def elevenlabs_voice_to_voice_info(voice_data: Dict[str, Any]) -> VoiceInfo:
    """Convert an ElevenLabs voice dict to a normalized VoiceInfo."""
    gender_map = {"male": VoiceGender.MALE, "female": VoiceGender.FEMALE}
    raw_gender = voice_data.get("labels", {}).get("gender", "neutral")
    gender = gender_map.get(raw_gender, VoiceGender.NEUTRAL)

    return VoiceInfo(
        voice_id=voice_data.get("voice_id", ""),
        name=voice_data.get("name", ""),
        language_code=voice_data.get("labels", {}).get("language", "en"),
        gender=gender,
        description=voice_data.get("description"),
        labels=voice_data.get("labels", {}),
        category=voice_data.get("category", "premade"),
    )
