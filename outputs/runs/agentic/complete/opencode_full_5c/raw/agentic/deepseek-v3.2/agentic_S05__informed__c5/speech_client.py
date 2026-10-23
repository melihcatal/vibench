import os
import azure.cognitiveservices.speech as speechsdk


class SpeechClient:
    """Provide local configuration and client helper utilities for Streaming Speech-to-Text."""

    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")

        if not self.speech_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable is required")
        if not self.speech_region:
            raise ValueError("AZURE_SPEECH_REGION environment variable is required")

        # Initialize Azure Speech SDK
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

        # Store SDK module for easy access
        self.speech = speechsdk
        self.audio = speechsdk.audio

    def create_recognizer(
        self,
        language="en-US",
        enable_punctuation=True,
        enable_word_timestamps=True,
        audio_config=None,
    ):
        """Create a speech recognizer with given configuration."""
        config = self.speech.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )
        config.speech_recognition_language = language

        if enable_punctuation:
            config.enable_dictation()

        if enable_word_timestamps:
            config.request_word_level_timestamps()

        if not audio_config:
            audio_config = self.audio.AudioConfig(use_default_microphone=True)

        return self.speech.SpeechRecognizer(
            speech_config=config, audio_config=audio_config
        )

    def create_push_stream_recognizer(self, language="en-US", enable_punctuation=True):
        """Create a recognizer with push audio stream."""
        config = self.speech.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )
        config.speech_recognition_language = language

        if enable_punctuation:
            config.enable_dictation()
            config.set_property(
                self.speech.PropertyId.SpeechServiceResponse_RequestPunctuation, "true"
            )

        push_stream = self.audio.PushAudioInputStream()
        audio_config = self.audio.AudioConfig(stream=push_stream)

        recognizer = self.speech.SpeechRecognizer(
            speech_config=config, audio_config=audio_config
        )

        return recognizer, push_stream

    def get_supported_languages(self):
        """Get list of supported languages for speech recognition."""
        # Azure Speech supports many languages, return a subset
        return {
            "en-US": "English (United States)",
            "en-GB": "English (United Kingdom)",
            "es-ES": "Spanish (Spain)",
            "es-MX": "Spanish (Mexico)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "it-IT": "Italian (Italy)",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian",
            "zh-CN": "Chinese (Mandarin, Simplified)",
            "zh-TW": "Chinese (Taiwanese Mandarin)",
        }

    def validate_audio_format(self, sample_rate=16000, channels=1, bits_per_sample=16):
        """Validate audio format compatibility with Azure Speech."""
        supported_formats = {
            "sample_rates": [8000, 16000, 32000, 44100, 48000],
            "channels": [1, 2],
            "bits_per_sample": [8, 16],
        }

        if sample_rate not in supported_formats["sample_rates"]:
            raise ValueError(
                f"Sample rate {sample_rate} not supported. Supported: {supported_formats['sample_rates']}"
            )

        if channels not in supported_formats["channels"]:
            raise ValueError(
                f"Channels {channels} not supported. Supported: {supported_formats['channels']}"
            )

        if bits_per_sample not in supported_formats["bits_per_sample"]:
            raise ValueError(
                f"Bits per sample {bits_per_sample} not supported. Supported: {supported_formats['bits_per_sample']}"
            )

        return True


# Singleton instance
_speech_client_instance = None


def get_speech_client():
    """Get or create the speech client instance."""
    global _speech_client_instance
    if _speech_client_instance is None:
        _speech_client_instance = SpeechClient()
    return _speech_client_instance
