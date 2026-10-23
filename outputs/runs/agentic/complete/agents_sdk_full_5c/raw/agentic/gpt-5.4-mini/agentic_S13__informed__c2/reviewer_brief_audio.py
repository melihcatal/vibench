from __future__ import annotations

from pathlib import Path

from elevenlabs import ElevenLabs

from safety_models import AudioBrief


client = ElevenLabs(api_key="ELEVENLABS_API_KEY")


def reviewer_brief_audio(text: str, output_path: str = "reviewer_brief.mp3") -> AudioBrief:
    audio = client.text_to_speech.convert(text=text, voice_id="Rachel", model_id="eleven_multilingual_v2")
    path = Path(output_path)
    with path.open("wb") as f:
        for chunk in audio:
            f.write(chunk)
    return AudioBrief(audio_path=str(path), text=text, provider="ElevenLabs")
