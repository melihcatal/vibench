import os

import azure.cognitiveservices.speech as speechsdk


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.getenv('AZURE_SPEECH_KEY')
    region = config.get('region') or os.getenv('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('Missing Azure speech credentials')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    voice = config.get('voice') or os.getenv('AZURE_SPEECH_VOICE')
    if voice:
        speech_config.speech_synthesis_voice_name = voice
    return speech_config


def synthesize_with_sdk(speech_config, text=None, ssml=None, output_format=None):
    if output_format is not None:
        speech_config.set_speech_synthesis_output_format(output_format)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    if ssml is not None:
        return synthesizer.speak_ssml_async(ssml).get()
    return synthesizer.speak_text_async(text).get()


def voice_catalog(locale=None):
    voices = [
        {'name': 'en-US-JennyNeural', 'locale': 'en-US', 'gender': 'Female'},
        {'name': 'en-US-GuyNeural', 'locale': 'en-US', 'gender': 'Male'},
        {'name': 'en-GB-LibbyNeural', 'locale': 'en-GB', 'gender': 'Female'},
    ]
    if locale:
        return [voice for voice in voices if voice['locale'] == locale]
    return voices
