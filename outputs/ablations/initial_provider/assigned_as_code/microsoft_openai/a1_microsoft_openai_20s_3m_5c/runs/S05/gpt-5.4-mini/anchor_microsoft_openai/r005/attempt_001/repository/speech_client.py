import os

import azure.cognitiveservices.speech as speechsdk


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY')
    region = config.get('region') or os.environ.get('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('missing Azure Speech configuration')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    if config.get('language_code'):
        speech_config.speech_recognition_language = config['language_code']
    if config.get('enable_punctuation') is not None:
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
                                  'TrueText' if config['enable_punctuation'] else 'Off')
    return speech_config


def load_language_settings(payload=None):
    payload = payload or {}
    return {
        'language_code': payload.get('language_code', 'en-US'),
        'sample_rate_hz': payload.get('sample_rate_hz', 16000),
        'enable_punctuation': payload.get('enable_punctuation', True),
    }


def build_push_stream(sample_rate_hz):
    return speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(
        samples_per_second=sample_rate_hz, bits_per_sample=16, channels=1))
