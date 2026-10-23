from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import create_speech_config
from speech_models import StreamingSpeechConfig, TranscriptEvent, normalize_event


def stream_with_language(
    language: str, enable_punctuation: bool = True
) -> Iterator[TranscriptEvent]:
    speech_config = create_speech_config(
        StreamingSpeechConfig(language=language, enable_punctuation=enable_punctuation)
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    recognizer.start_continuous_recognition()
    return iter(())
