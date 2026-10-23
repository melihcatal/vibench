import os
from elevenlabs import Voice, VoiceSettings, generate
from elevenlabs.client import ElevenLabs


def generate_audio_brief(text_brief: str, output_path: str):
    """
    Generates a spoken brief from retrieved search results using ElevenLabs TTS.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(
        text=text_brief,
        voice=Voice(
            voice_id="Rachel",
            settings=VoiceSettings(
                stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
            ),
        ),
    )

    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
