from azure.cognitiveservices.speech import AudioConfig, SpeechConfig, SpeechSynthesizer


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    speech_config = SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_synthesis_voice_name = config.get('voice', 'en-US-JennyNeural')
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=AudioConfig(use_default_speaker=True))
    text = payload['text'] if isinstance(payload, dict) else str(payload)
    synthesizer.speak_text_async(text).get()
    return {'spoken': True}
