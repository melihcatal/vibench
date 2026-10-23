import os
from dataclasses import dataclass
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import AudioResponse, TextToSpeechRequest, SsmlRequest, VoiceSelectionRequest, VoiceInfo, VoiceListResponse


@dataclass
class SpeechConfig:
    subscription_key: str
    region: str
    default_voice: str = 'en-US-JennyNeural'


def load_config() -> SpeechConfig:
    key = os.environ.get('AZURE_SPEECH_KEY') or os.environ.get('AZURE_SPEECH_SUBSCRIPTION_KEY')
    region = os.environ.get('AZURE_SPEECH_REGION') or 'eastus'
    default_voice = os.environ.get('AZURE_SPEECH_VOICE') or 'en-US-JennyNeural'
    if not key:
        raise EnvironmentError('AZURE_SPEECH_KEY or AZURE_SPEECH_SUBSCRIPTION_KEY is required')
    return SpeechConfig(subscription_key=key, region=region, default_voice=default_voice)


def get_default_voice(locale: str | None = None) -> str:
    cfg = load_config()
    return cfg.default_voice


class AzureSpeechClient:
    def __init__(self, config: Optional[SpeechConfig] = None):
        self.config = config or load_config()
        self.speech_config = speechsdk.SpeechConfig(subscription=self.config.subscription_key, region=self.config.region)
        self.speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    def synthesize_text(self, request: TextToSpeechRequest) -> AudioResponse:
        self.speech_config.speech_synthesis_voice_name = request.voice or self.config.default_voice
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        result = synthesizer.speak_text_async(request.text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(str(result.reason))
        return AudioResponse(audio_bytes=bytes(result.audio_data), content_type='audio/mpeg')

    def synthesize_ssml(self, request: SsmlRequest) -> AudioResponse:
        self.speech_config.speech_synthesis_voice_name = request.voice or self.config.default_voice
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        result = synthesizer.speak_ssml_async(request.ssml).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(str(result.reason))
        return AudioResponse(audio_bytes=bytes(result.audio_data), content_type='audio/mpeg')

    def list_voices(self, request: VoiceSelectionRequest) -> VoiceListResponse:
        voices = [
            VoiceInfo(name='en-US-JennyNeural', locale='en-US', gender='Female', provider='azure'),
            VoiceInfo(name='en-US-GuyNeural', locale='en-US', gender='Male', provider='azure'),
            VoiceInfo(name='en-GB-SoniaNeural', locale='en-GB', gender='Female', provider='azure'),
        ]
        if request.locale:
            voices = [v for v in voices if v.locale.lower() == request.locale.lower()]
        if request.gender:
            voices = [v for v in voices if v.gender.lower() == request.gender.lower()]
        if request.name:
            voices = [v for v in voices if request.name.lower() in v.name.lower()]
        return VoiceListResponse(voices=voices)


def get_tts_client() -> AzureSpeechClient:
    return AzureSpeechClient()
