from __future__ import annotations

from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from speech_client import create_push_stream, create_speech_config
from speech_models import StreamingRecognitionConfig


class LanguageAwareStreamingRecognizer:
    def __init__(
        self,
        *,
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        sample_rate_hz: int = 16000,
    ) -> None:
        self.config = StreamingRecognitionConfig(
            sample_rate_hz=sample_rate_hz,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )
        self.push_stream, audio_config = create_push_stream(sample_rate_hz=sample_rate_hz)
        speech_config = create_speech_config(self.config)
        speech_config.speech_recognition_language = language_code
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
            "TrueText",
        )
        speech_config.set_property(
            speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs,
            "700",
        )
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )

    def start(self) -> speechsdk.SpeechRecognizer:
        self.recognizer.start_continuous_recognition()
        return self.recognizer

    def stop(self) -> None:
        self.push_stream.close()
        self.recognizer.stop_continuous_recognition()
