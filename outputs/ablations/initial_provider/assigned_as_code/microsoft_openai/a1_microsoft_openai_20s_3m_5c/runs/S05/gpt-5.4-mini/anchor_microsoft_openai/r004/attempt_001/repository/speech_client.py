import os

import azure.cognitiveservices.speech as speechsdk


def load_speech_config(config=None):
    config = config or {}
    api_key = config.get('api_key') or os.getenv('AZURE_SPEECH_KEY')
    region = config.get('region') or os.getenv('AZURE_SPEECH_REGION')
    if not api_key or not region:
        raise ValueError('Missing Azure Speech credentials')
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    voice = config.get('voice')
    if voice:
        speech_config.speech_synthesis_voice_name = voice
    return speech_config


def make_audio_stream(sample_rate_hz):
    return speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(samples_per_second=sample_rate_hz, bits_per_sample=16, channels=1))


def make_recognizer(payload, config=None):
    speech_config = load_speech_config(config)
    speech_config.speech_recognition_language = payload['language_code']
    audio_stream = make_audio_stream(payload['sample_rate_hz'])
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(stream=audio_stream))
    return speech_config, audio_stream, recognizer
