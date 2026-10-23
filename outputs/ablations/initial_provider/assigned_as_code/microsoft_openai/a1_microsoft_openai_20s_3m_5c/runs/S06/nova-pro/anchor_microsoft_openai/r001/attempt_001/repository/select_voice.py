import azure.cognitiveservices.speech as speechsdk

def select_voice(language_code, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    voices = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).get_voices()
    for voice in voices:
        if language_code in voice.short_name:
            return voice.short_name
    return None
