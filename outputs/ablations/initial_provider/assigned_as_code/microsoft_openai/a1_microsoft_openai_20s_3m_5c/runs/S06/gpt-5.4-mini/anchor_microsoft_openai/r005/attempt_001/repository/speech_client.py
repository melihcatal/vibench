import os

import azure.cognitiveservices.speech as speechsdk

from speech_models import SpeechRequest, normalize_locale, normalize_output_format, normalize_text, normalize_voice


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY')
    region = config.get('region') or os.environ.get('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    return speech_config


def build_request(payload, config=None):
    config = config or {}
    return SpeechRequest(
        text=normalize_text(payload),
        locale=normalize_locale(payload, config.get('locale', 'en-US')),
        voice=normalize_voice(payload, config.get('voice', 'en-US-JennyNeural')),
        content_type=normalize_output_format(payload, config.get('content_type', 'audio/mpeg')),
    )


def configure_voice(speech_config, voice_name):
    speech_config.speech_synthesis_voice_name = voice_name
    return speech_config


def configure_output_format(speech_config, content_type):
    mapping = {
        'audio/mpeg': speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3,
        'audio/wav': speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm,
    }
    speech_config.set_speech_synthesis_output_format(mapping.get(content_type, speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3))
    return speech_config
