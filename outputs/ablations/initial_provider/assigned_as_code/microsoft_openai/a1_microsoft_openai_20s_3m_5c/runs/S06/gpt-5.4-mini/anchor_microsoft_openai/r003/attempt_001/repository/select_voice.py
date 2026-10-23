import azure.cognitiveservices.speech as speechsdk

from speech_client import load_tts_config


def select_voice(payload, config=None):
    config = load_tts_config(config)
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    voices = speechsdk.SpeechSynthesizer.get_voices_async(speech_config, payload.get('locale')).get()
    selected = None
    for voice in voices.voices:
        if payload.get('voice') and voice.short_name == payload['voice']:
            selected = voice.short_name
            break
    if selected is None and voices.voices:
        selected = voices.voices[0].short_name
    return {'voices': [voice.short_name for voice in voices.voices], 'voice': selected}
