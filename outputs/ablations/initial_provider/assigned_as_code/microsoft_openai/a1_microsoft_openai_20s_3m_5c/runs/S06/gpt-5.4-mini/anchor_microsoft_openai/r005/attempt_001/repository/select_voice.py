import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config


def select_voice(payload, config=None):
    config = config or {}
    speech_config = load_speech_config(config)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    voices = synthesizer.get_voices_async(payload.get('locale', config.get('locale', 'en-US'))).get().voices
    if payload.get('voice'):
        for voice in voices:
            if voice.short_name == payload['voice']:
                return {'voice': voice.short_name, 'locale': voice.locale, 'name': voice.name}
    return {'voices': [{'voice': voice.short_name, 'locale': voice.locale, 'name': voice.name} for voice in voices]}
