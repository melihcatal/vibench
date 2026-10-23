from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    model: str = "latest_long"
    use_enhanced: bool = True
    diarization_speaker_count: Optional[int] = None
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = True


def get_speech_client():
    """Initialize and return a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()


def get_audio_config(config: SpeechConfig, audio_uri: str) -> types.RecognitionConfig:
    """Create a RecognitionConfig for Google Cloud Speech-to-Text."""
    return types.RecognitionConfig(
        language_code=config.language_code,
        model=config.model,
        use_enhanced=config.use_enhanced,
        enable_word_time_offsets=config.enable_word_time_offsets,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
        diarization_config=(
            types.SpeakerDiarizationConfig(
                enable_speaker_diarization=config.diarization_speaker_count is not None,
                min_speaker_count=config.diarization_speaker_count,
                max_speaker_count=config.diarization_speaker_count,
            )
            if config.diarization_speaker_count
            else None
        ),
        audio_channel_count=2 if "stereo" in audio_uri.lower() else 1,
    )


def get_recognition_audio(audio_uri: str) -> types.RecognitionAudio:
    """Create a RecognitionAudio object for Google Cloud Speech-to-Text."""
    if audio_uri.startswith("gs://"):
        return types.RecognitionAudio(uri=audio_uri)
    else:
        with open(audio_uri, "rb") as audio_file:
            content = audio_file.read()
        return types.RecognitionAudio(content=content)
