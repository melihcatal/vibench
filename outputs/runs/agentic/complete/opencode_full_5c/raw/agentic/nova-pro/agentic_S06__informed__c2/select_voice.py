from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


def select_voice(locale):
    speech_key, service_region = get_speech_credentials()
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
    voices = speech_synthesizer.get_voices()
    for voice in voices.voices:
        if voice.locale.lower() == locale.lower():
            return voice.short_name
    return None


def get_speech_credentials():
    import os

    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    return speech_key, service_region
