import os
from dataclasses import dataclass
from typing import Optional

from elevenlabs.client import ElevenLabs


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ["ELEVENLABS_API_KEY"],
        voice_id=os.environ.get("ELEVENLABS_VOICE_ID", "Rachel"),
        model_id=os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
        output_format=os.environ.get("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"),
    )


def create_client(api_key: Optional[str] = None) -> ElevenLabs:
    return ElevenLabs(api_key=api_key or os.environ["ELEVENLABS_API_KEY"])


def get_voice_id(voice_id: Optional[str] = None) -> str:
    return voice_id or os.environ.get("ELEVENLABS_VOICE_ID", "Rachel")


def synthesize_text(text: str, voice_id: Optional[str] = None, model_id: Optional[str] = None) -> bytes:
    config = load_speech_config()
    client = create_client(config.api_key)
    audio = client.text_to_speech.convert(
        voice_id=get_voice_id(voice_id),
        model_id=model_id or config.model_id,
        text=text,
        output_format=config.output_format,
    )
    if isinstance(audio, bytes):
        return audio
    return b"".join(audio)
