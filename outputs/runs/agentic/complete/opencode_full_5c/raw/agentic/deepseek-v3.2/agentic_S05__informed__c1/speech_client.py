import os
from typing import Dict, Any, Optional
from deepgram import Deepgram


class SpeechClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable not set")
        self.client = Deepgram(self.api_key)

    def get_default_options(self) -> Dict[str, Any]:
        return {
            "model": "nova-2",
            "interim_results": True,
            "smart_format": True,
            "encoding": "linear16",
            "sample_rate": 16000,
            "channels": 1,
            "punctuate": True,
            "utterances": True,
            "diarize": False,
        }

    def get_language_options(self, language_code: str = "en") -> Dict[str, Any]:
        language_map = {
            "en": "en-US",
            "es": "es-419",
            "fr": "fr-FR",
            "de": "de-DE",
            "ja": "ja-JP",
            "zh": "zh-CN",
            "ko": "ko-KR",
            "pt": "pt-BR",
            "ru": "ru-RU",
            "ar": "ar-SA",
        }

        options = self.get_default_options()
        options["language"] = language_map.get(language_code, "en-US")
        return options

    def create_streaming_connection(
        self, custom_options: Optional[Dict[str, Any]] = None
    ):
        options = self.get_default_options()
        if custom_options:
            options.update(custom_options)

        return self.client.transcription.live(options)

    @staticmethod
    def normalize_audio_format(audio_format: str) -> str:
        format_map = {
            "wav": "linear16",
            "pcm": "linear16",
            "mp3": "mp3",
            "ogg": "ogg",
            "flac": "flac",
            "mulaw": "mulaw",
            "alaw": "alaw",
        }
        return format_map.get(audio_format.lower(), "linear16")

    @staticmethod
    def validate_sample_rate(sample_rate: int) -> int:
        supported_rates = [8000, 16000, 24000, 32000, 44100, 48000]
        if sample_rate in supported_rates:
            return sample_rate
        closest = min(supported_rates, key=lambda x: abs(x - sample_rate))
        return closest

    @staticmethod
    def load_config_from_env() -> Dict[str, Any]:
        config = {
            "api_key": os.getenv("DEEPGRAM_API_KEY"),
            "default_model": os.getenv("DEEPGRAM_MODEL", "nova-2"),
            "default_language": os.getenv("DEEPGRAM_LANGUAGE", "en-US"),
            "enable_smart_format": os.getenv("DEEPGRAM_SMART_FORMAT", "true").lower()
            == "true",
            "enable_diarization": os.getenv("DEEPGRAM_DIARIZE", "false").lower()
            == "true",
        }
        return config
