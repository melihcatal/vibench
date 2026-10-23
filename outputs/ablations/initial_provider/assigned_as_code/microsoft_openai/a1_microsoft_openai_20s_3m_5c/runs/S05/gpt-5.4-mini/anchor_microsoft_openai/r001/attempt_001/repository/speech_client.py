import os

import azure.cognitiveservices.speech as speechsdk


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY')
    region = config.get('region') or os.environ.get('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    if config.get('language_code'):
        speech_config.speech_recognition_language = config['language_code']
    if config.get('enable_punctuation'):
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, 'TrueText')
    return speech_config


def normalize_transcript(text):
    return (text or '').strip()
