from elevenlabs import generate, save, VoiceSettings, set_api_key
import os

set_api_key(os.getenv("ELEVENLABS_API_KEY"))


def reviewer_brief_audio(
    text: str, voice: str = "Rachel", output_file: str = "reviewer_brief.mp3"
) -> str:
    """
    Generate spoken briefs for moderation reviewers using ElevenLabs TTS.
    """
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.5, similarity_boost=0.5, style=0.5, use_speaker_boost=True
        ),
    )
    save(audio, output_file)
    return output_file
