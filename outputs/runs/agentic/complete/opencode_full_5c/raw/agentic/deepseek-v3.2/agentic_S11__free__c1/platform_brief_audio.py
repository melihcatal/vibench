import os
from typing import Dict, Any
from elevenlabs import generate, save
from model_models import PlatformResponse


def generate_spoken_briefing(
    response: PlatformResponse, voice_id: str = "Rachel"
) -> Dict[str, Any]:
    """Generate spoken briefings from platform outputs using ElevenLabs text-to-speech."""
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    try:
        audio = generate(
            text=response.content[:1000],
            voice=voice_id,
            model="eleven_monolingual_v1",
            api_key=elevenlabs_api_key,
        )

        output_filename = f"briefing_{response.model_id.replace('-', '_')}.mp3"
        save(audio, output_filename)

        return {
            "provider": "elevenlabs",
            "tts_model": "eleven_monolingual_v1",
            "voice_id": voice_id,
            "original_model": response.model_id,
            "audio_file": output_filename,
            "text_length": len(response.content[:1000]),
            "service": "ElevenLabs Text-to-Speech",
        }

    except Exception as e:
        return {
            "provider": "elevenlabs",
            "tts_model": "eleven_monolingual_v1",
            "original_model": response.model_id,
            "audio_generation": "failed",
            "error": str(e),
        }


def list_available_voices() -> Dict[str, Any]:
    """List available ElevenLabs voices."""
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    try:
        from elevenlabs import voices

        voices_list = voices(api_key=elevenlabs_api_key)

        voice_info = []
        for voice in voices_list:
            voice_info.append(
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category,
                    "labels": voice.labels,
                }
            )

        return {
            "provider": "elevenlabs",
            "voice_count": len(voice_info),
            "voices": voice_info[:10],
        }

    except Exception as e:
        return {"provider": "elevenlabs", "voice_listing": "failed", "error": str(e)}
