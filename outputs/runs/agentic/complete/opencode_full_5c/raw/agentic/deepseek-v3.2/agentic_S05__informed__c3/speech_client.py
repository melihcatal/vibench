import os
from typing import Optional, Dict, Any
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
    CancellationReason,
    SpeechSynthesisOutputFormat,
)
from azure.cognitiveservices.speech.audio import (
    PushAudioInputStream,
    PullAudioInputStream,
)


class SpeechClient:
    def __init__(self, api_key: Optional[str] = None, region: Optional[str] = None):
        self.api_key = api_key or os.environ.get("AZURE_SPEECH_KEY")
        self.region = region or os.environ.get("AZURE_SPEECH_REGION")

        if not self.api_key:
            raise ValueError(
                "Azure Speech API key not provided. Set AZURE_SPEECH_KEY environment variable."
            )
        if not self.region:
            raise ValueError(
                "Azure Speech region not provided. Set AZURE_SPEECH_REGION environment variable."
            )

        self._speech_config = None
        self._recognizer = None
        self._push_stream = None

    def create_speech_config(self, language: str = "en-US", **kwargs) -> SpeechConfig:
        config = SpeechConfig(subscription=self.api_key, region=self.region)
        config.speech_recognition_language = language

        if kwargs.get("enable_punctuation", True):
            config.set_property(
                property_id="SpeechServiceResponse_RequestPunctuation", value="true"
            )

        if kwargs.get("profanity_filter", True):
            from azure.cognitiveservices.speech import ProfanityOption

            config.set_profanity(ProfanityOption.Masked)

        if kwargs.get("word_level_timestamps", False):
            config.request_word_level_timestamps()

        if kwargs.get("enable_dictation", False):
            config.enable_dictation()

        config.output_format = SpeechSynthesisOutputFormat.Detailed

        self._speech_config = config
        return config

    def create_push_stream(self) -> PushAudioInputStream:
        self._push_stream = PushAudioInputStream()
        return self._push_stream

    def create_recognizer(
        self,
        audio_config: Optional[AudioConfig] = None,
        speech_config: Optional[SpeechConfig] = None,
    ) -> SpeechRecognizer:
        if speech_config is None:
            speech_config = self.create_speech_config()

        if audio_config is None:
            if self._push_stream is None:
                self._push_stream = self.create_push_stream()
            audio_config = AudioConfig(stream=self._push_stream)

        self._recognizer = SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )
        return self._recognizer

    def cleanup(self):
        if self._recognizer:
            try:
                self._recognizer.stop_continuous_recognition()
            except:
                pass

        if self._push_stream:
            try:
                self._push_stream.close()
            except:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


class SpeechConfigLoader:
    @staticmethod
    def from_env() -> Dict[str, Any]:
        return {
            "api_key": os.environ.get("AZURE_SPEECH_KEY"),
            "region": os.environ.get("AZURE_SPEECH_REGION"),
            "language": os.environ.get("SPEECH_LANGUAGE", "en-US"),
            "enable_punctuation": os.environ.get(
                "SPEECH_ENABLE_PUNCTUATION", "true"
            ).lower()
            == "true",
            "profanity_filter": os.environ.get(
                "SPEECH_PROFANITY_FILTER", "true"
            ).lower()
            == "true",
            "word_level_timestamps": os.environ.get(
                "SPEECH_WORD_TIMESTAMPS", "false"
            ).lower()
            == "true",
        }

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        required = ["api_key", "region"]
        return all(config.get(key) for key in required)


class AudioFormat:
    @staticmethod
    def get_default_format() -> Dict[str, Any]:
        return {
            "sample_rate": 16000,
            "channels": 1,
            "bits_per_sample": 16,
            "format": "pcm",
        }

    @staticmethod
    def validate_audio_chunk(chunk: bytes, expected_format: Dict[str, Any]) -> bool:
        if not chunk:
            return False

        sample_rate = expected_format.get("sample_rate", 16000)
        channels = expected_format.get("channels", 1)
        bits_per_sample = expected_format.get("bits_per_sample", 16)

        bytes_per_sample = bits_per_sample // 8
        expected_chunk_size = sample_rate * channels * bytes_per_sample // 100

        return len(chunk) <= expected_chunk_size * 2


class RecognitionResultParser:
    @staticmethod
    def parse_azure_result(result) -> Dict[str, Any]:
        if result.reason == ResultReason.RecognizedSpeech:
            return {
                "text": result.text,
                "is_final": True,
                "confidence": result.confidence,
                "duration": result.duration.total_seconds()
                if result.duration
                else None,
                "offset": result.offset / 10000000 if result.offset else None,
                "language": result.properties.get("language", ""),
                "reason": "RecognizedSpeech",
            }
        elif result.reason == ResultReason.RecognizingSpeech:
            return {
                "text": result.text,
                "is_final": False,
                "confidence": result.confidence,
                "duration": result.duration.total_seconds()
                if result.duration
                else None,
                "offset": result.offset / 10000000 if result.offset else None,
                "language": result.properties.get("language", ""),
                "reason": "RecognizingSpeech",
            }
        elif result.reason == ResultReason.NoMatch:
            return {
                "text": "",
                "is_final": False,
                "confidence": 0.0,
                "reason": "NoMatch",
                "details": result.no_match_details,
            }
        elif result.reason == ResultReason.Canceled:
            cancellation = result.cancellation_details
            return {
                "text": "",
                "is_final": False,
                "reason": "Canceled",
                "error_code": cancellation.error_code.value
                if cancellation.error_code
                else None,
                "error_details": cancellation.error_details,
                "reason_text": cancellation.reason.value
                if cancellation.reason
                else None,
            }
        else:
            return {
                "text": "",
                "is_final": False,
                "reason": "Unknown",
                "raw_result": str(result),
            }


def create_speech_client_from_env() -> SpeechClient:
    config = SpeechConfigLoader.from_env()
    if not SpeechConfigLoader.validate_config(config):
        raise ValueError(
            "Missing required Azure Speech configuration in environment variables"
        )

    return SpeechClient(api_key=config["api_key"], region=config["region"])


def get_available_languages() -> Dict[str, str]:
    return {
        "en-US": "English (United States)",
        "en-GB": "English (United Kingdom)",
        "es-ES": "Spanish (Spain)",
        "fr-FR": "French (France)",
        "de-DE": "German (Germany)",
        "it-IT": "Italian (Italy)",
        "ja-JP": "Japanese",
        "ko-KR": "Korean",
        "zh-CN": "Chinese (Mandarin)",
        "ru-RU": "Russian",
    }
