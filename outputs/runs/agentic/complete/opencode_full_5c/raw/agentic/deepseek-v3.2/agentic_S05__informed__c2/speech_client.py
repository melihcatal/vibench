import azure.cognitiveservices.speech as speechsdk
import os
from typing import Optional, Dict, Any


class SpeechClient:
    def __init__(
        self, speech_key: Optional[str] = None, speech_region: Optional[str] = None
    ):
        self.speech_key = speech_key or os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = speech_region or os.getenv("AZURE_SPEECH_REGION")

        if not self.speech_key or not self.speech_region:
            raise ValueError(
                "Azure Speech credentials not found. "
                "Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables."
            )

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

        self.default_language = "en-US"
        self.enable_punctuation = True
        self.enable_word_timestamps = True

    def create_audio_config(
        self, use_microphone: bool = True, audio_file: Optional[str] = None
    ):
        if use_microphone and not audio_file:
            return speechsdk.audio.AudioConfig(use_default_microphone=True)
        elif audio_file:
            return speechsdk.audio.AudioConfig(filename=audio_file)
        else:
            return speechsdk.audio.AudioConfig(use_default_microphone=True)

    def create_recognizer(
        self,
        language_code: str = None,
        audio_config: Optional[speechsdk.audio.AudioConfig] = None,
    ):
        if language_code:
            self.speech_config.speech_recognition_language = language_code
        else:
            self.speech_config.speech_recognition_language = self.default_language

        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestPunctuation,
            "true" if self.enable_punctuation else "false",
        )

        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps,
            "true" if self.enable_word_timestamps else "false",
        )

        if not audio_config:
            audio_config = self.create_audio_config()

        return speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

    def create_push_stream_recognizer(self):
        push_stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        return recognizer, push_stream

    def configure_streaming(
        self,
        language_code: str = "en-US",
        enable_punctuation: bool = True,
        enable_word_timestamps: bool = True,
        profanity_filter: str = "masked",
    ):
        self.speech_config.speech_recognition_language = language_code
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestPunctuation,
            "true" if enable_punctuation else "false",
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps,
            "true" if enable_word_timestamps else "false",
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_ProfanityOption, profanity_filter
        )

        self.default_language = language_code
        self.enable_punctuation = enable_punctuation
        self.enable_word_timestamps = enable_word_timestamps

    def get_supported_languages(self) -> Dict[str, str]:
        return {
            "en-US": "English (United States)",
            "en-GB": "English (United Kingdom)",
            "es-ES": "Spanish (Spain)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "it-IT": "Italian (Italy)",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese (Mandarin, Simplified)",
            "zh-TW": "Chinese (Mandarin, Traditional)",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian",
            "ar-SA": "Arabic (Saudi Arabia)",
            "hi-IN": "Hindi (India)",
        }

    def validate_language(self, language_code: str) -> bool:
        supported = self.get_supported_languages()
        return language_code in supported

    def get_audio_format(self) -> speechsdk.audio.AudioStreamFormat:
        return speechsdk.audio.AudioStreamFormat.get_wave_format_pcm(
            samples_per_second=16000, bits_per_sample=16, channels=1
        )

    @staticmethod
    def load_environment():
        required_vars = ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]
        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return {
            "speech_key": os.getenv("AZURE_SPEECH_KEY"),
            "speech_region": os.getenv("AZURE_SPEECH_REGION"),
        }
