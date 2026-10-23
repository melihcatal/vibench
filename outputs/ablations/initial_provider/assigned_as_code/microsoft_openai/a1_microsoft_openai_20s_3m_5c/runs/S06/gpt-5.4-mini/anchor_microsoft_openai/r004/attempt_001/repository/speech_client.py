import os
import azure.cognitiveservices.speech as speechsdk


def load_tts_config(config=None):
    config = dict(config or {})
    if 'api_key' not in config:
        config['api_key'] = os.environ.get('AZURE_SPEECH_KEY')
    if 'region' not in config:
        config['region'] = os.environ.get('AZURE_SPEECH_REGION')
    if 'voice' not in config:
        config['voice'] = os.environ.get('AZURE_SPEECH_VOICE', 'en-US-JennyNeural')
    return config


def build_speech_config(config=None):
    config = load_tts_config(config)
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    if config.get('voice'):
        speech_config.speech_synthesis_voice_name = config['voice']
    return speech_config


def build_synthesizer(config=None, audio_config=None):
    return speechsdk.SpeechSynthesizer(speech_config=build_speech_config(config), audio_config=audio_config)
