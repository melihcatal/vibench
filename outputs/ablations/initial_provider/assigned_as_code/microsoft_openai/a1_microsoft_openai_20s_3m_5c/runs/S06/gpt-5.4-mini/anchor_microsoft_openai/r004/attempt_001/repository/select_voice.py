import azure.cognitiveservices.speech as speechsdk

from speech_models import normalize_voice_request


def select_voice(payload, config=None):
    config = normalize_voice_request(payload, config)
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    voices = speechsdk.SpeechSynthesizer.get_voices_async(speech_config, config.get('locale')).get()
    if not voices.voices:
        raise RuntimeError('No voices available')
    selected = config.get('voice') or voices.voices[0].short_name
    return {'voice': selected, 'voices': [voice.short_name for voice in voices.voices]}
