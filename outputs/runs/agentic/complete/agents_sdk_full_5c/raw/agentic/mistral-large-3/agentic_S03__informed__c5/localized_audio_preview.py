from elevenlabs import Voice, VoiceSettings, generate, save
from typing import Optional


class ElevenLabsAudioPreviewGenerator:
    def __init__(self):
        self.default_voice_id = "pNInz6obpgDQGcFmaJgB"  # Example voice ID

    def generate_audio_preview(self, text: str, voice_id: Optional[str] = None) -> bytes:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=voice_id or self.default_voice_id,
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True),
            ),
        )
        return audio

    def save_audio_preview(self, text: str, output_path: str, voice_id: Optional[str] = None) -> None:
        audio = self.generate_audio_preview(text, voice_id)
        save(audio, output_path)


def generate_localized_audio_preview(text: str, output_path: str, voice_id: Optional[str] = None) -> None:
    generator = ElevenLabsAudioPreviewGenerator()
    generator.save_audio_preview(text, output_path, voice_id)