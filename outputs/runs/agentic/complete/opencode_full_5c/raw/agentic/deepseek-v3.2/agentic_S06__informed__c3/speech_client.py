import os
import azure.cognitiveservices.speech as speechsdk
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SpeechConfig:
    speech_key: str
    speech_region: str
    default_voice: str = "en-US-JennyNeural"
    default_output_format: str = "riff-16khz-16bit-mono-pcm"

    @classmethod
    def from_env(cls):
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        speech_region = os.environ.get("AZURE_SPEECH_REGION")

        if not speech_key or not speech_region:
            raise ValueError(
                "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
            )

        return cls(
            speech_key=speech_key,
            speech_region=speech_region,
            default_voice=os.environ.get(
                "AZURE_SPEECH_DEFAULT_VOICE", "en-US-JennyNeural"
            ),
            default_output_format=os.environ.get(
                "AZURE_SPEECH_OUTPUT_FORMAT", "riff-16khz-16bit-mono-pcm"
            ),
        )


class SpeechClient:
    def __init__(self, config: Optional[SpeechConfig] = None):
        if config is None:
            config = SpeechConfig.from_env()

        self.config = config
        self._speech_config = None
        self._synthesizer = None

    @property
    def speech_config(self):
        if self._speech_config is None:
            self._speech_config = speechsdk.SpeechConfig(
                subscription=self.config.speech_key, region=self.config.speech_region
            )
            self._speech_config.speech_synthesis_voice_name = self.config.default_voice
            self._speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat[self.config.default_output_format]
            )
        return self._speech_config

    @property
    def synthesizer(self):
        if self._synthesizer is None:
            self._synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, audio_config=None
            )
        return self._synthesizer

    def create_synthesizer_with_voice(self, voice_name: str):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.config.speech_key, region=self.config.speech_region
        )
        speech_config.speech_synthesis_voice_name = voice_name
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat[self.config.default_output_format]
        )

        return speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None
        )

    def get_available_voices(self, locale_filter: Optional[str] = None):
        result = self.synthesizer.get_voices_async().get()

        voices = []
        for voice in result.voices:
            voice_info = {
                "name": voice.short_name,
                "locale": voice.locale,
                "gender": voice.gender.name if voice.gender else "Unknown",
                "voice_type": voice.voice_type.name if voice.voice_type else "Unknown",
            }

            if locale_filter:
                if voice.locale.startswith(locale_filter):
                    voices.append(voice_info)
            else:
                voices.append(voice_info)

        return voices

    def validate_voice(self, voice_name: str) -> bool:
        voices = self.get_available_voices()
        return any(v["name"] == voice_name for v in voices)

    def get_supported_locales(self):
        voices = self.get_available_voices()
        locales = set(v["locale"] for v in voices)
        return sorted(list(locales))


def get_default_client() -> SpeechClient:
    return SpeechClient()
