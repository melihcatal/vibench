import os
import elevenlabs

def localized_audio_preview(text: str, lang: str = "en") -> bytes:
    """
    Generate spoken preview of translated copy using ElevenLabs TTS.
    """
    elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    # Multilingual voice IDs: Rachel for many languages
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel
    audio = elevenlabs.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        output_format="mp3_22050_32"
    )
    return audio
