import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class AudioPreview:
    text: str
    language: str
    audio_data: bytes
    audio_format: str
    voice_id: str
    model_id: str


@dataclass
class AudioPreviewBatch:
    previews: List[AudioPreview] = field(default_factory=list)
    total_duration_estimate_ms: int = 0


def generate_audio_preview(
    text: str,
    language: str = "en",
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> AudioPreview:
    from elevenlabs import ElevenLabs, VoiceSettings

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set")

    client = ElevenLabs(api_key=api_key)

    voice_settings = VoiceSettings(
        stability=stability,
        similarity_boost=similarity_boost,
    )

    audio_generator = client.generate(
        text=text,
        voice=voice_id,
        model=model,
        output_format=output_format,
        voice_settings=voice_settings,
    )

    audio_chunks = list(audio_generator)
    audio_data = b"".join(audio_chunks)

    return AudioPreview(
        text=text,
        language=language,
        audio_data=audio_data,
        audio_format=output_format,
        voice_id=voice_id,
        model_id=model,
    )


def generate_audio_previews_batch(
    texts: List[str],
    languages: Optional[List[str]] = None,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> AudioPreviewBatch:
    from elevenlabs import ElevenLabs, VoiceSettings

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set")

    client = ElevenLabs(api_key=api_key)

    if languages is None:
        languages = ["en"] * len(texts)

    voice_settings = VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
    )

    previews = []
    total_duration_ms = 0

    for i, text in enumerate(texts):
        language = languages[i] if i < len(languages) else "en"

        audio_generator = client.generate(
            text=text,
            voice=voice_id,
            model=model,
            output_format=output_format,
            voice_settings=voice_settings,
        )

        audio_chunks = list(audio_generator)
        audio_data = b"".join(audio_chunks)

        estimated_ms = int(len(text) * 60)
        total_duration_ms += estimated_ms

        preview = AudioPreview(
            text=text,
            language=language,
            audio_data=audio_data,
            audio_format=output_format,
            voice_id=voice_id,
            model_id=model,
        )
        previews.append(preview)

    return AudioPreviewBatch(
        previews=previews,
        total_duration_estimate_ms=total_duration_ms,
    )
