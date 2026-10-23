import os

import azure.cognitiveservices.speech as speechsdk


def load_tts_config(config=None):
    config = config or {}
    return {
        'api_key': config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY'),
        'region': config.get('region') or os.environ.get('AZURE_SPEECH_REGION'),
        'voice': config.get('voice') or os.environ.get('AZURE_SPEECH_VOICE', 'en-US-JennyNeural'),
    }


def create_speech_config(config=None):
    config = load_tts_config(config)
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_synthesis_voice_name = config['voice']
    return speech_config


def synthesize_text_with_config(text, config=None):
    speech_config = create_speech_config(config)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure speech synthesis failed')
    return result.audio_data
