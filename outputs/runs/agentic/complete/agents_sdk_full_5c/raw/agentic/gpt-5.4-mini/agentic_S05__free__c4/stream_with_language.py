from __future__ import annotations

from typing import Iterable, Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, microphone_requests
from speech_models import SpeechStreamConfig


def stream_with_language(audio_frames: Iterable[bytes], language_code: str = "en-US") -> Iterator[str]:
    client = build_client()
    config = SpeechStreamConfig(language_code=language_code, punctuation=True, interim_results=True)
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )
    for response in client.streaming_recognize(streaming_config, microphone_requests(audio_frames)):
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
