import os
from typing import AsyncIterable, Optional

from google.cloud import speech_v1p1beta1 as speech


def build_recognition_config(language_code: Optional[str] = None, enable_punctuation: bool = True) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE_HZ", "16000")),
        language_code=language_code or os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US"),
        enable_automatic_punctuation=enable_punctuation,
        model=os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
        audio_channel_count=int(os.getenv("GOOGLE_CLOUD_SPEECH_CHANNELS", "1")),
    )


def start_streaming_recognizer(audio_chunks: AsyncIterable[bytes], language_code: Optional[str] = None, enable_punctuation: bool = True):
    client = speech.SpeechClient()
    config = build_recognition_config(language_code=language_code, enable_punctuation=enable_punctuation)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    async def requests():
        async for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    return client.streaming_recognize(streaming_config, requests())
