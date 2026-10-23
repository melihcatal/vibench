# Generate spoken previews of translated copy using ElevenLabs Text to Speech
import os
from typing import List
from elevenlabs import Voice, VoiceSettings, generate, save
from elevenlabs.client import ElevenLabs


def generate_localized_audio_preview(texts: List[str], output_dir: str) -> List[str]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    client = ElevenLabs(api_key=api_key)
    voice = Voice(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Predefined voice ID for "Adam"
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
    )

    file_paths = []
    for i, text in enumerate(texts):
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        file_path = f"{output_dir}/preview_{i}.mp3"
        save(audio, file_path)
        file_paths.append(file_path)

    return file_paths