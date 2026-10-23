from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def select_voice(locale: str):
    speech_key = "YOUR_AZURE_SPEECH_KEY"
    service_region = "YOUR_AZURE_SPEECH_REGION"

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config)

    voices = synthesizer.get_voices()
    for voice in voices.voices:
        if voice.locale == locale:
            return voice.short_name
    return None