import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def generate_localized_audio_preview(text: str, lang: str, output_path: str) -> None:
    """
    Generates spoken previews of translated copy using ElevenLabs TTS.
    """
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Multilingual voice (Rachel)
    model_id = "eleven_multilingual_v2"
    audio = client.text_to_speech.convert(
        text=text, voice_id=voice_id, model_id=model_id
    )
    save(audio, output_path)
