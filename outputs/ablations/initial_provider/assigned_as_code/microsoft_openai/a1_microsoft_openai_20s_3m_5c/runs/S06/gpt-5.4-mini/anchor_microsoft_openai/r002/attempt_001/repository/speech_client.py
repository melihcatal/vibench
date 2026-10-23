import os

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat, AudioConfig, SpeechRecognizer


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.getenv('AZURE_SPEECH_KEY')
    region = config.get('region') or os.getenv('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('Azure Speech API key and region are required')
    speech_config = SpeechConfig(subscription=api_key, region=region)
    if config.get('voice'):
        speech_config.speech_synthesis_voice_name = config['voice']
    output_format = config.get('output_format', SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    speech_config.set_speech_synthesis_output_format(output_format)
    return speech_config


def build_synthesizer(config=None, audio_config=None):
    return SpeechSynthesizer(speech_config=load_speech_config(config), audio_config=audio_config)


def build_recognizer(config=None, audio_config=None):
    return SpeechRecognizer(speech_config=load_speech_config(config), audio_config=audio_config)


def to_audio_config(path=None):
    if path:
        return AudioConfig(filename=path)
    return None
