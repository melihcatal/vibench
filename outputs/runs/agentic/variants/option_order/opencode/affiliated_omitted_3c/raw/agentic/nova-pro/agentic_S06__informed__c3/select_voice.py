from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer


def select_voice(locale):
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    voices = synthesizer.get_voices(locale)
    return voices
