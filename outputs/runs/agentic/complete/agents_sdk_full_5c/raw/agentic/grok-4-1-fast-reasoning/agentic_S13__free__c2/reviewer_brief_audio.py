import os
from elevenlabs import generate, save, VoiceSettings
from elevenlabs.client import ElevenLabs

def generate_reviewer_brief_audio(brief_text: str, output_path: str) -> None:
    """
    Generates spoken briefs for moderation reviewers using ElevenLabs TTS.
    """
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    voice = "Rachel"
    settings = VoiceSettings(stability=0.5, similarity_boost=0.75)

    audio = client.generate(
        text=brief_text,
        voice=voice,
        model="eleven_multilingual_v2",
        voice_settings=settings
    )
    with open(output_path, "wb") as f:
        f.write(audio)
