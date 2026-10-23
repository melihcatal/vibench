import os
from typing import Optional, Dict, Any
from google.cloud import speech
from google.oauth2 import service_account


class SpeechClientConfig:
    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ):

        self.credentials_path = credentials_path
        self.project_id = project_id
        self.api_key = api_key

        if credentials_path and os.path.exists(credentials_path):
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
        elif api_key:
            self.credentials = None
        else:
            self.credentials = None

    def get_client(self) -> speech.SpeechClient:
        if self.credentials:
            return speech.SpeechClient(credentials=self.credentials)
        else:
            return speech.SpeechClient()

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        api_key = os.environ.get("GOOGLE_SPEECH_API_KEY")

        return cls(
            credentials_path=credentials_path, project_id=project_id, api_key=api_key
        )

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "SpeechClientConfig":
        return cls(
            credentials_path=config_dict.get("credentials_path"),
            project_id=config_dict.get("project_id"),
            api_key=config_dict.get("api_key"),
        )


class StreamingSpeechClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None):
        self.config = config or SpeechClientConfig.from_env()
        self.client = self.config.get_client()

    def create_recognition_config(
        self,
        language_code: str = "en-US",
        sample_rate_hertz: int = 16000,
        encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation: bool = True,
        model: str = "latest_long",
        use_enhanced: bool = False,
        **kwargs,
    ) -> speech.RecognitionConfig:

        return speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            model=model,
            use_enhanced=use_enhanced,
            **{k: v for k, v in kwargs.items() if hasattr(speech.RecognitionConfig, k)},
        )

    def create_streaming_config(
        self,
        recognition_config: speech.RecognitionConfig,
        interim_results: bool = True,
        single_utterance: bool = False,
    ) -> speech.StreamingRecognitionConfig:

        return speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=interim_results,
            single_utterance=single_utterance,
        )

    def validate_audio_format(
        self, sample_rate: int, encoding: speech.RecognitionConfig.AudioEncoding
    ) -> bool:
        supported_sample_rates = [8000, 16000, 24000, 32000, 44100, 48000]

        if sample_rate not in supported_sample_rates:
            print(
                f"Warning: Sample rate {sample_rate}Hz may not be optimal. Supported: {supported_sample_rates}"
            )
            return False

        supported_encodings = [
            speech.RecognitionConfig.AudioEncoding.LINEAR16,
            speech.RecognitionConfig.AudioEncoding.FLAC,
            speech.RecognitionConfig.AudioEncoding.MULAW,
            speech.RecognitionConfig.AudioEncoding.AMR,
            speech.RecognitionConfig.AudioEncoding.AMR_WB,
            speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            speech.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE,
        ]

        if encoding not in supported_encodings:
            print(f"Warning: Encoding {encoding} may not be supported")
            return False

        return True

    def get_supported_languages(self) -> Dict[str, str]:
        return {
            "en-US": "English (United States)",
            "en-GB": "English (Great Britain)",
            "es-ES": "Spanish (Spain)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "ja-JP": "Japanese (Japan)",
            "ko-KR": "Korean (South Korea)",
            "zh-CN": "Chinese (Mandarin, Simplified)",
            "zh-TW": "Chinese (Mandarin, Traditional)",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian (Russia)",
            "it-IT": "Italian (Italy)",
            "nl-NL": "Dutch (Netherlands)",
            "ar-SA": "Arabic (Saudi Arabia)",
            "hi-IN": "Hindi (India)",
        }

    def check_client_connection(self) -> bool:
        try:
            self.client.get_operation(name="test")
            return True
        except:
            try:
                test_config = self.create_recognition_config()
                return True
            except Exception as e:
                print(f"Client connection check failed: {e}")
                return False


class AudioStreamHelper:
    @staticmethod
    def chunk_audio_data(audio_data: bytes, chunk_size: int = 4096) -> list:
        return [
            audio_data[i : i + chunk_size]
            for i in range(0, len(audio_data), chunk_size)
        ]

    @staticmethod
    def calculate_duration(
        audio_data: bytes, sample_rate: int = 16000, sample_width: int = 2
    ) -> float:
        num_samples = len(audio_data) / sample_width
        return num_samples / sample_rate

    @staticmethod
    def normalize_audio_level(audio_data: bytes, target_level: float = 0.8) -> bytes:
        import numpy as np
        import struct

        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        max_val = np.max(np.abs(audio_array))

        if max_val > 0:
            scale_factor = target_level * 32767 / max_val
            scaled_audio = np.clip(audio_array * scale_factor, -32768, 32767)
            return scaled_audio.astype(np.int16).tobytes()

        return audio_data
